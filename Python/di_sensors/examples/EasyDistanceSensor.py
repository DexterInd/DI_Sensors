#!/usr/bin/env python
#
# https://www.dexterindustries.com
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# Python example program for the Dexter Industries Distance Sensor

# import the modules
from di_sensors.easy_distance_sensor import EasyDistanceSensor
from time import sleep

# instantiate the distance object
my_sensor = EasyDistanceSensor()

# and read the sensor iteratively
try:
    while True:
        read_distance = my_sensor.read()
        print("distance from object: {} cm".format(read_distance))
        sleep(0.1)
except KeyboardInterrupt:
    pass
