## Python Library for Temperature_Pressure_Humidity Sensor

The Temperature_Pressure_Humidity Sensor connects with the GrovePi,GoPiGo and PivotPi.

This sensor uses a BME280 chip to measure the Temperature, Pressure and Humidity.

**_Files:_**
- **BME280.py** : Main Python library to read data from BME280 chip
- **temp_press_humidity.py** : Python Library to provide the basic functions for using the Temperature_Pressure_Humidity Sensor
- **example.py** : Example to test all the basic functions of the Temperature_Pressure_Humidity Sensor
- **setup.py** : Installation file for the Temperature_Pressure_Humidity Sensor (use only if you are not using Dexter Industries SD Card)
- **requirements.txt** : Additional packages to be installed by the script setup.py.
- **I2C.py** : Library to handle I2C communication across platforms.
- **Platform.py** : Script to detect the platform in which the sensor is used.

#Installation
setup.py is the install script for the Temperature_Pressure_Humidity Sensor which installs all the packages and libraries need for running the Sensor.
To install setup.py run (use only if you are not using Dexter Industries SD Card):
> sudo python setup.py install

## Getting Help
Need help? We [have a forum here where you can ask questions or make suggestions](http://forum.dexterindustries.com/)


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

