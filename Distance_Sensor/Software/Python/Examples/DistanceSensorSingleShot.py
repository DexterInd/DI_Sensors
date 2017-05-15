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
import distance_sensor

sensor = distance_sensor.DistanceSensor()

'''
if LONG_RANGE:
  # lower the return signal rate limit (default is 0.25 MCPS)
  sensor.setSignalRateLimit(0.1)
  # increase laser pulse periods (defaults are 14 and 10 PCLKs)
  sensor.setVcselPulsePeriod(VcselPeriodPreRange, 18)
  sensor.setVcselPulsePeriod(VcselPeriodFinalRange, 14)

if HIGH_SPEED:
    # reduce timing budget to 20 ms (default is about 33 ms)
    sensor.setMeasurementTimingBudget(20000)
elif HIGH_ACCURACY:
    # increase timing budget to 200 ms
    sensor.setMeasurementTimingBudget(200000)
'''

while True:
    print("%4dmm" % sensor.readRangeSingleMillimeters())
    if sensor.timeoutOccurred():
        print(" TIMEOUT")
