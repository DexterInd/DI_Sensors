#!/usr/bin/env python
#
# https://www.dexterindustries.com/GoPiGo/
# https://github.com/DexterInd/DI_Sensors
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/GoPiGo3/blob/master/LICENSE.md

try:
	with open('package_description.rst', 'r') as file_description:
		description = file_description.read()

except IOError:
	print(str(IOError))
	print("make sure you have [package_description.rst] file in the same directory as [setup.py]")

from setuptools import setup, find_packages
setup(
    name = "DI_Sensors",
    version = "1.0.0",

    description = "Drivers and examples for using DI_Sensors in Python",
    long_description = description,

    author = "Dexter Industries",
    author_email = "contact@dexterindustries.com",

    license = "MIT",
    classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'License :: OSI Approved :: MIT License',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development :: Embedded Systems',
    'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    url = "https://github.com/DexterInd/DI_Sensors",

    keywords = [
        "Dexter",
        "Distance Sensor",
        "Inertial Measurement Unit",
        "IMU",
        "Light Color Sensor",
        "Temperature Humidity Pressure Sensor",
        "RGB LCD",
        "DHT Sensor",
    ],
    packages = find_packages(),
	install_requires = ["python-periphery"]
)

#install_requires=open('requirements.txt').readlines(),
