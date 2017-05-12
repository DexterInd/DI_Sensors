#!/usr/bin/env python
#
# https://www.dexterindustries.com/GoPiGo/
# https://github.com/DexterInd/DI_Sensors
#
# Copyright (c) 2016 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/GoPiGo3/blob/master/LICENSE.md

import setuptools
setuptools.setup(
    name="DI_Sensors",
    description="Drivers and examples for using the DI_Sensors in Python",
    author="Dexter Industries",
    url="http://www.dexterindustries.com/DI_Sensors/",
    package_dir = {"grove_rgb_lcd" : "grove_rgb_lcd/", "distance_sensor" : "Distance_Sensor/Software/Python", "dht" : "DHT_Sensor/",},
    packages=["grove_rgb_lcd", "distance_sensor", "dht"]
    #install_requires=open('requirements.txt').readlines(),
)
