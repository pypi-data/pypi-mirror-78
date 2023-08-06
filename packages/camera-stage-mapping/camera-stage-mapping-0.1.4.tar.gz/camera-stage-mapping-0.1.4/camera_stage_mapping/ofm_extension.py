"""
OpenFlexure Microscope API extension for stage calibration

This file contains the HTTP API for camera/stage calibration. It
includes calibration functions that measure the relationship between
stage coordinates and camera coordinates, as well as functions that
move by a specified displacement in pixels, perform closed-loop moves,
and return the calibration data.

This module is only intended to be called from the OpenFlexure Microscope
server, and depends on that server and its underlying LabThings library.
"""
from labthings.views import ActionView, PropertyView
from labthings.find import find_component
from labthings.extensions import BaseExtension
from labthings import fields

from labthings.utilities import get_by_path, set_by_path, create_from_path

from flask import abort, send_file

import logging
import time
import numpy as np
import PIL
import io
import os
import json
from collections import namedtuple

from .camera_stage_calibration_1d import (
    calibrate_backlash_1d,
    image_to_stage_displacement_from_1d,
)
from .camera_stage_tracker import Tracker
from .closed_loop_move import closed_loop_move, closed_loop_scan
from .scan_coords_times import ordered_spiral

from openflexure_microscope.utilities import axes_to_array
from openflexure_microscope.paths import data_file_path
from openflexure_microscope.config import JSONEncoder

CSM_DATAFILE_NAME = "csm_calibration.json"
CSM_DATAFILE_PATH = data_file_path(CSM_DATAFILE_NAME)

MoveHistory = namedtuple("MoveHistory", ["times", "stage_positions"])
class LoggingMoveWrapper():
    """Wrap a move function, and maintain a log position/time.
    
    This class is callable, so it doesn't change the signature
    of the function it wraps - it just makes it possible to get
    a list of all the moves we've made, and how long they took.
    
    Said list is intended to be useful for calibrating the stage
    so we can estimate how long moves will take.
    """
    def __init__(self, move_function):
        self._move_function = move_function
        self._current_position = None
        self.clear_history()

    def __call__(self, new_position, *args, **kwargs):
        """Move to a new position, and record it"""
        self._history.append((time.time(), self._current_position))
        self._move_function(new_position, *args, **kwargs)
        self._current_position = new_position
        self._history.append((time.time(), self._current_position))

    @property
    def history(self):
        """The history, as a numpy array of times and another of positions"""
        times = np.array([t for t, p in self._history])
        positions = np.array([p for t, p in self._history])
        return MoveHistory(times, positions)

    def clear_history(self):
        """Reset our history to be an empty list"""
        self._history = []


class CSMExtension(BaseExtension):
    """
    Use the camera as an encoder, so we can relate camera and stage coordinates
    """

    def __init__(self):
        BaseExtension.__init__(
            self,
            "org.openflexure.camera_stage_mapping",
            version="0.0.1",
        )

    _microscope = None

    @property
    def microscope(self):
        # TODO: does caching the microscope actually help?
        if self._microscope is None:
            self._microscope = find_component("org.openflexure.microscope")
        return self._microscope
    
    def update_settings(self, settings):
        """Update the stored extension settings dictionary"""
        keys = ["extensions", self.name]
        dictionary = create_from_path(keys)
        set_by_path(dictionary, keys, settings)
        logging.info(f"Updating settings with {dictionary}")
        self.microscope.update_settings(dictionary)
        self.microscope.save_settings()

    def get_settings(self):
        """Retrieve the settings for this extension"""
        keys = ["extensions", self.name]
        return get_by_path(self.microscope.read_settings(), keys)

    def camera_stage_functions(self):
        """Return functions that allow us to interface with the microscope"""
        self.microscope.camera.start_worker()  # ensure the worker thread is running, so there is an MJPEG stream
        
        def grab_image():
            jpeg = self.microscope.camera.get_frame()
            return np.array(PIL.Image.open(io.BytesIO(jpeg)))
        
        def get_position():
            return self.microscope.stage.position
        
        move = self.microscope.stage.move_abs
        
        def wait():
            time.sleep(0.2)

        return grab_image, get_position, move, wait

    def calibrate_1d(self, direction):
        """Move a microscope's stage in 1D, and figure out the relationship with the camera"""
        grab_image, get_position, move, wait = self.camera_stage_functions()
        move = LoggingMoveWrapper(move)  # log positions and times for stage calibration

        tracker = Tracker(grab_image, get_position, settle=wait)

        result = calibrate_backlash_1d(tracker, move, direction)
        result["move_history"] = move.history
        return result

    def calibrate_xy(self):
        """Move the microscope's stage in X and Y, to calibrate its relationship to the camera"""
        logging.info("Calibrating X axis:")
        cal_x = self.calibrate_1d(np.array([1, 0, 0]))
        logging.info("Calibrating Y axis:")
        cal_y = self.calibrate_1d(np.array([0, 1, 0]))
        
        # Combine X and Y calibrations to make a 2D calibration
        cal_xy = image_to_stage_displacement_from_1d([cal_x, cal_y])
        self.update_settings(cal_xy)

        data = {
            "camera_stage_mapping_calibration": cal_xy,
            "linear_calibration_x": cal_x,
            "linear_calibration_y": cal_y,
        }

        with open(CSM_DATAFILE_PATH, "w") as f:
            json.dump(data, f, cls=JSONEncoder)

        return data

    @property
    def image_to_stage_displacement_matrix(self):
        """A 2x2 matrix that converts displacement in image coordinates to stage coordinates."""
        try:
            settings = self.get_settings()
            return settings["image_to_stage_displacement"]
        except KeyError:
            raise ValueError("The microscope has not yet been calibrated.")

    def move_in_image_coordinates(self, displacement_in_pixels):
        """Move by a given number of pixels on the camera"""
        p = np.array(displacement_in_pixels)
        relative_move = np.dot(p, self.image_to_stage_displacement_matrix)
        self.microscope.stage.move_rel([relative_move[0], relative_move[1], 0])

    def closed_loop_move_in_image_coordinates(self, displacement_in_pixels, **kwargs):
        """Move by a given number of pixels on the camera, using the camera as an encoder."""
        grab_image, get_position, move, wait = self.camera_stage_functions()

        tracker = Tracker(grab_image, get_position, settle=wait)
        tracker.acquire_template()
        closed_loop_move(tracker, self.move_in_image_coordinates, displacement_in_pixels, **kwargs)

    def closed_loop_scan(self, scan_path, **kwargs):
        """Perform closed-loop moves to each point defined in scan_path.

        This returns a generator, which will move the stage to each point in
        ``scan_path``, then yield ``i, pos`` where ``i``
        is the index of the scan point, and ``pos`` is the estimated position
        in pixels relative to the starting point.  To use it properly, you 
        should iterate over it, for example::
        
            for i, pos in csm_extension.closed_loop_scan(scan_path):
                capture_image(f"image_{i}.jpg")

        ``scan_path`` should be an Nx2 numpy array defining
        the points to visit in pixels relative to the current position.

        If an exception occurs during the scan, we automatically return to the
        starting point.  Keyword arguments are passed to 
        ``closed_loop_move.closed_loop_scan``.
        """
        grab_image, get_position, move, wait = self.camera_stage_functions()

        tracker = Tracker(grab_image, get_position, settle=wait)
        tracker.acquire_template()

        return closed_loop_scan(tracker, self.move_in_image_coordinates, move, np.array(scan_path), **kwargs)


    def test_closed_loop_spiral_scan(self, step_size, N, **kwargs):
        """Move the microscope in a spiral scan, and return the positions."""
        scan_path = ordered_spiral(0,0, N, *step_size)

        for i, pos in self.closed_loop_scan(np.array(scan_path), **kwargs):
            pass


csm_extension = CSMExtension()

class Calibrate1DView(ActionView):
    args = {"direction": fields.List(fields.Float(), required=True, example=[1, 0, 0])}

    def post(self, args):
        """Calibrate one axis of the microscope stage against the camera."""
        
        direction = np.array(args.get("direction"))

        return csm_extension.calibrate_1d(direction)


csm_extension.add_view(Calibrate1DView, "/calibrate_1d", endpoint="calibrate_1d")


class CalibrateXYView(ActionView):
    def post(self):
        """Calibrate both axes of the microscope stage against the camera."""
        return csm_extension.calibrate_xy()


csm_extension.add_view(CalibrateXYView, "/calibrate_xy", endpoint="calibrate_xy")


class MoveInImageCoordinatesView(ActionView):
    args = {
        "x": fields.Float(description="The number of pixels to move in X", required=True, example=100),
        "y": fields.Float(description="The number of pixels to move in Y", required=True, example=100),
    }

    def post(self, args):
        logging.debug("moving in pixels")
        """Move the microscope stage, such that we move by a given number of pixels on the camera"""
        csm_extension.move_in_image_coordinates(
            np.array([args.get("x"), args.get("y")])
        )
        
        return csm_extension.microscope.state["stage"]["position"]

csm_extension.add_view(MoveInImageCoordinatesView, "/move_in_image_coordinates", endpoint="move_in_image_coordinates")


class ClosedLoopMoveInImageCoordinatesView(ActionView):
    args = {
        "x": fields.Float(description="The number of pixels to move in X", required=True, example=100),
        "y": fields.Float(description="The number of pixels to move in Y", required=True, example=100),
    }

    def post(self, args):
        logging.debug("moving in pixels")
        """Move the microscope stage, such that we move by a given number of pixels on the camera"""
        csm_extension.closed_loop_move_in_image_coordinates(np.array([args.get("x"), args.get("y")]))
        
        return csm_extension.microscope.state["stage"]["position"]

csm_extension.add_view(ClosedLoopMoveInImageCoordinatesView, "/closed_loop_move_in_image_coordinates")

class TestClosedLoopSpiralScanView(ActionView):
    args = {
        "x_step": fields.Float(description="The number of pixels to move in X", required=True, example=100),
        "y_step": fields.Float(description="The number of pixels to move in Y", required=True, example=100),
        "N": fields.Int(description="The number of rings in the spiral scan", required=True, example=3),
    }

    def post(self, args):
        logging.debug("moving in pixels")
        """Move the microscope stage, such that we move by a given number of pixels on the camera"""
        return csm_extension.test_closed_loop_spiral_scan(np.array([args.get("x"), args.get("y")]), args.get("N"))

csm_extension.add_view(TestClosedLoopSpiralScanView, "/test_closed_loop_spiral_scan", endpoint="test_closed_loop_spiral_scan")

class GetCalibrationFile(PropertyView):
    def get(self):
        """Get the calibration data in JSON format."""
        datafile_name = CSM_DATAFILE_NAME
        datafile_path = CSM_DATAFILE_PATH

        if os.path.isfile(datafile_path):
            with open(datafile_path, "rb") as f:
                return json.load(f)
        else:
            return {}


csm_extension.add_view(GetCalibrationFile, "/get_calibration", endpoint="get_calibration")