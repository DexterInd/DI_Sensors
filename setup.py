#!/usr/bin/env python
#
# https://www.dexterindustries.com/GoPiGo/
# https://github.com/DexterInd/DI_Sensors
#
# Copyright (c) 2016 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/GoPiGo3/blob/master/LICENSE.md

from setuptools import setup, find_packages
setup(
    name="DI_Sensors",
    license="MIT",
    description="Drivers and examples for using DI_Sensors in Python",
    author="Dexter Industries",
    version="1.0.0",
    keywords=[
        "Dexter",
        "Distance Sensor",
        "DHT Sensor",
        "Color Light Sensor",
        "IMU",
        "Temperature Humidity Pressure Sensor"
    ],
    url="http://www.dexterindustries.com/DI_Sensors/",
    packages=find_packages()

)
#    package_dir = {"grove_rgb_lcd" : "grove_rgb_lcd/", "distance_sensor" : "Distance_Sensor/Software/Python", "DHT" : "DHT_Sensor/",},
    # packages=["grove_rgb_lcd", "distance_sensor", "DHT"]
    #install_requires=open('requirements.txt').readlines(),
