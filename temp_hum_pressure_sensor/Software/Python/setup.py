#!/usr/bin/env python

import setuptools
setuptools.setup(
    name="temp_press_humidity",
    description="Drivers and examples for using the Temperature_Pressure_Humidity Sensor in Python",
    author="Dexter Industries",
    py_modules=['temp_press_humidity','BME280','I2C','Platform'],
    install_requires=open('requirements.txt').readlines(),
)
