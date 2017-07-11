# https://www.dexterindustries.com
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# Python drivers for the Dexter Industries Inertial Measurement Unit sensor

from __future__ import print_function
from __future__ import division

from di_sensors import BNO055


class InertialMeasurementUnit(object):
    def __init__(self, bus = "RPI_1"):
        """Initialize the sensor
        
        Keyword arguments:
        bus (default "RPI_1") -- The I2C bus"""
        try:
            self.BNO055 = BNO055.BNO055(bus = bus)
        except RuntimeError:
            raise RuntimeError('Failed to initialize Dexter Industries IMU sensor')
    
    def read_euler(self):
        """Read the absolute orientation
        
        Returns the current absolute orientation as a tuple of heading, roll, and pitch euler angles in degrees."""
        return  self.BNO055.read_euler()
    
    def read_magnetometer(self):
        """Read the magnetometer
        
        Returns the current magnetometer reading as a tuple of X, Y, Z values in micro-Teslas."""
        return self.BNO055.read_magnetometer()
    
    def read_gyroscope(self):
        """Read the gyroscope
        
        Returns the current gyroscope (angular velocity) reading as a tuple of X, Y, Z values in degrees per second."""
        return self.BNO055.read_gyroscope()
    
    def read_accelerometer(self):
        """Read the accelerometer
        
        Returns the current accelerometer reading as a tuple of X, Y, Z values in meters/second^2."""
        return self.BNO055.read_accelerometer()
    
    def read_linear_acceleration(self):
        """Read linear acceleration
        
        Returns the current linear acceleration (acceleration from movement not from gravity) reading as a tuple of X, Y, Z values in meters/second^2."""
        return self.BNO055.read_linear_acceleration()
    
    def read_gravity(self):
        """Read gravity
        
        Returns the current gravity reading as a tuple of X, Y, Z values in meters/second^2."""
        return self.BNO055.read_gravity()
    
    def read_quaternion(self):
        """Read the quaternion values
        
        Returns the current orientation as a tuple of X, Y, Z, W quaternion values."""
        return self.BNO055.read_quaternion()
    
    def read_temperature(self):
        """Read the temperature
        
        Returns the current temperature in degrees celsius."""
        return self.BNO055.read_temp()
