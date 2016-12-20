#!/usr/bin/env python
#
# Example for Temperature_Pressure_Humidity Sensor
#
# This example shows the methods to read the temperature, pressure and humidity using Temperature_Pressure_Humidity Sensor
#
# The Temperature_Pressure_Humidity Sensor connects with the GrovePi,GoPiGo and PivotPi.
#
# This sensor uses a BME280 chip to measure the Temperature, Pressure and Humidity.
#
# Have a question about this example?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
#
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

from __future__ import print_function
from __future__ import division
from builtins import input
# the above lines are meant for Python3 compatibility.
# they force the use of Python3 functionality for print(), 
# the integer division and input()
# mind your parentheses!

import temp_press_humidity

try:
    sensor = temp_press_humidity.temp_press_humidity(0x76)
    print('Temperature  = %s deg C'%(sensor.temp_celcius()))
    print('Temperature  = %s deg F'%(sensor.temp_fahrenheit()))
    print('Pressure     = %s Pascals'%(sensor.press()))
    print('Humidity     = %s %% '%(sensor.humidity()))
except IOError:
    print("Sensor not found - quitting")
    exit(-1)
