#!/usr/bin/env python
#
# Python example for the DI color sensor
#
# This example is derived from Adafruit's library for TCS34725 color sensor here: https://github.com/adafruit/Adafruit_Python_TCS34725
'''
## License
The MIT License (MIT)

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
import time
import di_color_sensor

cs = di_color_sensor.color_sensor() 
while True:
    # Read the R, G, B, C color data.
    r, g, b, c = cs.get_raw_colors()

    # Calculate color temperature
    color_temp = cs.color_temperature()

    # Calculate lux
    lux = cs.luminosity()

    # Print out the values.
    print('Color: red={0} green={1} blue={2} clear={3}'.format(r, g, b, c))

    # Print out color temperature.
    if color_temp is None:
        print('Too dark to determine color temperature!')
    else:
        print('Color Temperature: {0} K'.format(color_temp))

    # Print out the lux.
    print('Luminosity: {0} lux\n'.format(lux))