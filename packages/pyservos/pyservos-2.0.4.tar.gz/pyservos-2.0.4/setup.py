# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyservos', 'pyservos.bin']

package_data = \
{'': ['*']}

install_requires = \
['colorama', 'pyserial']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata']}

entry_points = \
{'console_scripts': ['servoAX12 = pyservos.bin.servoAX12:main']}

setup_kwargs = {
    'name': 'pyservos',
    'version': '2.0.4',
    'description': 'Yet another dynamixel python driver',
    'long_description': '![](https://raw.githubusercontent.com/MultipedRobotics/pyservos/master/pics/dynamixel.jpg)\n\n[![CheckPackage](https://github.com/MultipedRobotics/pyservos/workflows/CheckPackage/badge.svg)](https://github.com/MultipedRobotics/pyservos/actions)\n![GitHub](https://img.shields.io/github/license/multipedrobotics/pyservos)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyservos)\n![PyPI](https://img.shields.io/pypi/v/pyservos)\n\n# pyServos\n\n**Still under development**\n**Starting to add XL-430 servo**\n\n- pyservos\n    - **ServoSerial** - half duplex hardware serial interface using DTR from a USB serial port\n    - **PiServoSerial** - half duplex hardware serial interface using a HW pin\n    - **utils** - misc\n    - **XL320** - register/command/error definitions for Dynamixel\'s XL-320 servo\n    - **AX12** - register/command/error definitions for Dynamixel\'s AX-12A servo\n    - **XL430** - register/command/error definitions for Dynamixel\'s AX-12A servo\n\n# Setup\n\n## Install\n\nThe suggested way to install this is via the `pip` command as follows::\n\n    pip install pyservos\n\n## Development\n\nI am currently using [poetry](https://python-poetry.org/) for my library and using\n`pyproject.toml`. To submit git pulls, clone the repository and set it up as\nfollows:\n\n    git clone https://github.com/MultipedRobotics/pyservos\n    cd pyservos\n    poetry install\n    poety run pytest\n\n# Usage\n\nThe `\\bin` directory has a number of useful programs to set servo position or ID number. Just\nrun the command with the `--help` flag to see how to use it.\n\n- `servoAX12`\n- `servoXL320` (not implemented)\n- `servoXL430` (not implemented)\n\nThe above commands have the following format:\n\n - servoXXX\n    - **ping**: find servos on bus, ID[int|**None**]\n    - **reboot**: reboot a servo, ID[int|**None**]\n    - **reset**: reset a servo, ID[int], level[int]\n    - **angle**: set new angle in degrees or radians, angle[float], radians[True|**False**]\n    - **baudrate**: set new baudrate, rate[int]\n    - **id**: set new ID, current_id[int], new_id[int]\n- Values\n    - ID: 1-254\n    - reset level: 1 (all), 2(all but ID), 3 (all but ID and baudrate)\n    - angle: 0-300 degrees\n    - rate: 1000000 is default\n    - None: if you leave out the value, there is a default that occurs which is safe\n\n# Documentation\n\n- [AX-12A Servo](https://github.com/MomsFriendlyRobotCompany/pyservos/tree/master/docs/ax12)\n- [XL-320 Servo](https://github.com/MomsFriendlyRobotCompany/pyservos/tree/master/docs/xl320)\n- [XL-430 Servo](https://github.com/MomsFriendlyRobotCompany/pyservos/tree/master/docs/xl430)\n\nA simple example to turn the servo and turn the LED on using a USB serial converter:\n\n```python\n# Run an AX-12 servo\nfrom pyservos.servo_serial import ServoSerial\nfrom pyservos.ax12 import AX12\n\nserial = ServoSerial(\'/dev/tty.usbserial\')  # tell it what port you want to use\n# serial = ServoSerial(\'dummy\')  # use a dummy serial interface for testing\nserial.open()\n\nax = AX12()\npkt = ax.makeServoPacket(1, 158.6)  # move servo 1 to 158.6 degrees\nret = serial.sendPkt(pkt)  # send packet, I don\'t do anything with the returned status packet\n\npkt = ax.makeLEDPacket(1, AX12.LED_ON)\nret = serial.sendPkt(pkt)\n```\n\nAlthough I have made some packet creators (like LED and Servo), you can make\nyour own using the basic `makeWritePacket` and `makeReadPacket`.\n\n```python\n# Run an XL-320 servo\nfrom pyservos.xl320 import XL320\nfrom pyservos.utils import angle2int\n\nxl = XL320()\n\n# let\'s make our own servo packet that sends servo 3 to 220.1 degrees\nID = 3\nreg = XL320.GOAL_POSITION\nparams = angle2int(220.1)  # convert 220.1 degrees to an int between 0-1023\npkt = xl.makeWritePacket(ID, reg, params)\n```\n\n## Dynaixel Servos\n\n![](pics/dynamixel-chart.jpg)\n\n![](pics/dynamixel-connectors.jpg)\n\n## Robot Examples\n\nHere are some example [robots](https://github.com/MultipedRobotics/pyservos/tree/master/docs/robots)\n\n# Other Software\n\nI haven\'t used these, but they seem good:\n\n- c++: [libdynamixel](https://github.com/resibots/libdynamixel)\n\n# Change Log\n\n| | | |\n|------------|-------|--------------------------------------------|\n| 2020-01-25 | 2.0.0 | re-architected around protocols rather than servos types |\n| 2018-04-30 | 1.0.1 |  API fixes and starting to add 430 support |\n| 2018-02-17 | 1.0.0 |  added AX-12 support and renamed the library |\n| 2017-04-01 | 0.9.0 |  added python3 support |\n| 2017-03-26 | 0.8.0 |  major overhaul and removed the GPIO stuff |\n| 2017-03-19 | 0.7.7 |  can switch between GPIO pin and pyserial.setRTS() |\n| 2017-02-20 | 0.7.6 |  small fixes and added servo_reboot |\n| 2017-01-16 | 0.7.5 |  fixes some small errors |\n| 2016-11-29 | 0.7.4 |  add bulk write and small changes |\n| 2016-10-11 | 0.7.1 |  small changes/updates |\n| 2016-09-12 | 0.7.0 |  refactoring, still working on API |\n| 2016-09-05 | 0.5.0 |  published to PyPi |\n| 2016-08-16 | 0.0.1 |  init |\n\n# The MIT License (MIT)\n\nCopyright (c) 2016 Kevin J. Walchko\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of\nthis software and associated documentation files (the "Software"), to deal in\nthe Software without restriction, including without limitation the rights to\nuse, copy, modify, merge, publish, distribute, sublicense, and/or sell copies\nof the Software, and to permit persons to whom the Software is furnished to do\nso, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS\nFOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR\nCOPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER\nIN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN\nCONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n',
    'author': 'walchko',
    'author_email': 'walchko@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/pyservos/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
