# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['camera_stage_mapping']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.17,<2.0']

extras_require = \
{'all': ['opencv-python-headless>=4.1,<5.0', 'scipy>=1.4,<2.0'],
 'correlation': ['opencv-python-headless>=4.1,<5.0', 'scipy>=1.4,<2.0']}

setup_kwargs = {
    'name': 'camera-stage-mapping',
    'version': '0.1.4',
    'description': 'Calibration and mapping between stage and camera coordinates in a microscope',
    'long_description': "# Camera Stage Mapping calibration\n\nThis Python module allows you to calibrate a microscope's stage against the camera.  By moving the sample a known number of steps, and tracking how far the image translates, it is possible to recover the number of steps per pixel.  This code goes a step further, and recovers a 2x2 affine transformation matrix, so it will cope with rotation, flipping, and non-uniform scaling of the X and Y axes.  The calibration routines are designed to be relatively robust and minimally parameterised, so they start by determining a sensible step size automatically.\n\nAs part of the calibration, you can use either FFT-based or directly calculated cross correlation to track motion of the sample.  This code is probably useful on its own, and is found in the ``fft_image_tracking`` and ``correlation_image_tracking`` submodules.  The underlying mechanism of tracking stage and camera coordinates simultaneously is handled by the ``CameraStageTracker`` class, in ``camera_stage_tracker``.  The main calibration function is ``camera_stage_calibration_1d.calibrate_backlash_1d``.  For 2D calibration, I recommend running this once for X and once for Y, then using ``camera_stage_calibration_1d.image_to_stage_displacement_from_1d`` to combine the two calibrations.  This is more robust than the 2D grid calibration method.\n\n## Hardware interface\nRather than tie these functions to a specific class interface, as found in many lab control frameworks, the calibration routines simply require functions to be passed in as arguments.  This is done for maximum flexibility, and to impose the fewest necessary constraints on the hardware we are controlling.  In the future, we may define a class interface to use, and would welcome input on how to do this without forcing a particular taxonomy of laboratory instruments upon everyone using the library.\n\n## Installing\n```\npip install camera-stage-mapping\n```\nThis package is published on PyPI and can be installed using ``pip``.  It's managed using ``poetry`` and can be installed by cloning the repository and running ``poetry install``.  For details of how to set up a development environment, please see [CONTRIBUTING].\n\n## Documentation\nThe functions all have fairly extensive docstrings and the module is documented on [readthedocs].\n\n[readthedocs]: https://camera-stage-mapping.readthedocs.io/en/latest/index.html\n[CONTRIBUTING]: ./CONTRIBUTING.md",
    'author': 'Richard Bowman',
    'author_email': 'richard.bowman@cantab.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/openflexure/microscope-extensions/camera-stage-mapping/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
