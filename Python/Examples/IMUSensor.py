#!/usr/bin/env python
#
# https://www.dexterindustries.com
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# Python example program for the Dexter Industries IMU Sensor

from __future__ import print_function
from __future__ import division

import time
from di_sensors import inertial_measurement_unit

print("Example program for reading a Dexter Industries IMU Sensor on a GoPiGo3 AD1 port.")

imu = inertial_measurement_unit.InertialMeasurementUnit(bus = "GPG3_AD1")

while True:
    # Read the magnetometer, gyroscope, accelerometer, euler, and temperature values
    mag   = imu.read_magnetometer()
    gyro  = imu.read_gyroscope()
    accel = imu.read_accelerometer()
    euler = imu.read_euler()
    temp  = imu.read_temperature()
    
    # Print the values
    print('Magnetometer X: %6.1f  Y: %6.1f  Z: %6.1f  Gyroscope X: %7.1f  Y: %7.1f  Z: %7.1f  Accelerometer X: %5.1f  Y: %5.1f  Z: %5.1f  Euler Heading: %5.1f  Roll: %5.1f  Pitch: %5.1f  Temperature: %5.1fC' % (mag[0], mag[1], mag[2], gyro[0], gyro[1], gyro[2], accel[0], accel[1], accel[2], euler[0], euler[1], euler[2], temp))
    
    time.sleep(0.1)
