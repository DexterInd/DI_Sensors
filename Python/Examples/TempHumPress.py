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

import time
from di_sensors.temp_hum_press import TempHumPress

print("Example program for reading a Dexter Industries Temperature Humidity Pressure Sensor on an I2C port.")

thp = TempHumPress()

while True:
    # Read the temperature
    temp = thp.get_temperature_celsius()

    # Read the relative humidity
    hum = thp.get_humidity()

    # Read the pressure
    press = thp.get_pressure()

    # Print the values
    print("Temperature: {:5.3f} Humidity: {:5.3f} Pressure: {:5.3f}".format(temp, hum, press))

    time.sleep(0.02)
