#!/usr/bin/env python
#
# Python library for the DI color sensor
# v0.0.1
#
# This library is derived from Adafruit's library for TCS34725 color sensor here: https://github.com/adafruit/Adafruit_Python_TCS34725
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
# Initial Authoring: 15 Dec 2016
# Last Updated: 15 Dec 2016
# http://www.dexterindustries.com/
# Date      		Comments
# 15 Dec 2016 		Initial Authoring

import TCS34725

# Time to wait refers to the integration_time for the sensor which impacts the resolution and the sensitivity of the RGBC reading. 
TIME_TO_WAIT_2_4MS  = 0xFF   #  2.4ms - 1 cycle    - Max Count: 1024
TIME_TO_WAIT_24MS   = 0xF6   # 24ms  - 10 cycles  - Max Count: 10240
TIME_TO_WAIT_50MS   = 0xEB   #  50ms  - 20 cycles  - Max Count: 20480
TIME_TO_WAIT_101MS  = 0xD5   #  101ms - 42 cycles  - Max Count: 43008
TIME_TO_WAIT_154MS  = 0xC0   #  154ms - 64 cycles  - Max Count: 65535
TIME_TO_WAIT_700MS  = 0x00   #  700ms - 256 cycles - Max Count: 65535

# Control the sensitivity of the color sensor. Higher the gain, more fine is the difference is between the dark and light conditions
SENSITIVITY_1X                  = 0x00   #  No gain
SENSITIVITY_4X                  = 0x01   #  2x gain
SENSITIVITY_16X                 = 0x02   #  16x gain
SENSITIVITY_60X                 = 0x03   #  60x gain

class color_sensor(object): 
	def __init__(self,
				time_to_wait=TIME_TO_WAIT_101MS,
				sensitivity=SENSITIVITY_16X):
		self.color_sensor_obj = TCS34725.TCS34725(integration_time=time_to_wait,gain=sensitivity)
	
	# returns RGBC values after a wait specified by the integration time
	def get_raw_colors(self):
		return self.color_sensor_obj.get_raw_data()
	
	# converts RGB values to color temperature in Kelivns
	# 6500K to 3000K check here for details wikipedia.org/wiki/Color_temperature
	def color_temperature(self):
		r,g,b,c= self.get_raw_colors()
		return TCS34725.calculate_color_temperature(r,g,b)
		
	# returns the luminosity in Lux
	def luminosity(self):
		r,g,b,c= self.get_raw_colors()
		return TCS34725.calculate_lux(r, g, b)