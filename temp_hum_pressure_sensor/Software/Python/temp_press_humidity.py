#!/usr/bin/env python
#
# Temperature_Pressure_Humidity Sensor Python library
#
# This file provides the basic functions for using the Temperature_Pressure_Humidity Sensor
#
# The Temperature_Pressure_Humidity Sensor connects with the GrovePi,GoPiGo and PivotPi.
#
# This sensor uses a BME280 chip to measure the Temperature, Pressure and Humidity.
#
# Have a question about this example?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
#
# Initial Date: 15 Dec 2016
# Last Updated: 15 Dec 2016
# http://www.dexterindustries.com/
# Author        Date            Comments
# Shoban        15 Dec 2016     Initial Authoring

'''
## License
The MIT License (MIT)
Temperature_Pressure_Humidity Sensor: an open source sensor for connecting with GrovePi to measure the Temperature, Pressure and Humidity.
Copyright (C) 2016  Dexter Industries
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''


import BME280

class temp_press_humidity(object):
    sensor_bme280=None

    def __init__(self, addr = 0x76):# Set the address
        try:
            self.sensor_bme280 = BME280.BME280(address=addr)
        except:
            # pass
            raise IOError("Sensor not connected")
        return
    # To read the temperature in celcius
    def temp_celcius(self):
        try:
            temp=self.sensor_bme280.read_temperature()
            return '{:0.3f}'.format(temp)
        except:
            raise IOError("Sensor not connected")
    # To read the temperature in fahrenheit
    def temp_fahrenheit(self):
        try:
            fahrenheit= (self.sensor_bme280.read_temperature()*(9.0/5.0)+32.0)
            return '{0:0.3f}'.format(fahrenheit)
        except:
            raise IOError("Sensor not connected")
    # To read the pressure in pascals
    def press(self):
        try:
            press=self.sensor_bme280.read_pressure()
            return '{0:0.3f}'.format(press)
        except:
            raise IOError("Sensor not connected")

    # To read the Relative humidity in percentage
    def humidity(self):
        try:
            humidity=self.sensor_bme280.read_humidity()
            return '{0:0.3f}'.format(humidity)
        except:
            raise IOError("Sensor not connected")
