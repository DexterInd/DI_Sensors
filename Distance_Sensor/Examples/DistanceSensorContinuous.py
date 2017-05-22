#!/usr/bin/env python
#
# https://www.dexterindustries.com/
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/BrickPi3/blob/master/LICENSE.md
#
# Python example program for the VL53L0X Distance Sensor

import time
from Distance_Sensor import distance_sensor

sensor = distance_sensor.DistanceSensor()

# Start continuous back-to-back mode (take readings as
# fast as possible).  To use continuous timed mode
# instead, provide a desired inter-measurement period in
# ms (e.g. sensor.startContinuous(100)).
sensor.startContinuous()
while True:
    print("%4dmm" % sensor.readRangeContinuousMillimeters())
    if sensor.timeoutOccurred():
        print(" TIMEOUT")
