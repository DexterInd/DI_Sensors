#!/usr/bin/env python
#
# https://www.dexterindustries.com
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# Python example program for the Dexter Industries Temperature Humidity Pressure Sensor

from __future__ import print_function
from __future__ import division

from time import sleep
from di_sensors.easy_temp_hum_press import EasyTHPSensor

print("Example program for reading a Dexter Industries Temperature Humidity Pressure Sensor on an I2C port.")

my_thp = EasyTHPSensor()

while True:
    # Read the temperature
    temp = my_thp.safe_celsius()

    # Read the relative humidity
    hum = my_thp.safe_humidity()

    # Read the pressure
    press = my_thp.safe_pressure()

    # Print the values
    print("Temperature: {:5.3f} Humidity: {:5.3f} Pressure: {:5.3f}".format(temp, hum, press))

    sleep(0.02)
