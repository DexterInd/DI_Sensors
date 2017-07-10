# https://www.dexterindustries.com
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# Python drivers for the Dexter Industries Temperature Humidity Pressure Sensor

from __future__ import print_function
from __future__ import division

from DI_Sensors import BME280


class TempHumPress(object):
    """Drivers for the Dexter Industries Temperature Humidity Pressure Sensor"""
    
    def __init__(self, bus = "RPI_1"):
        """Initialize the sensor
        
        Keyword arguments:
        bus (default "RPI_1") -- The I2C bus"""
        self.BME280 = BME280.BME280(bus = bus, t_mode = BME280.OSAMPLE_2, p_mode = BME280.OSAMPLE_4, h_mode = BME280.OSAMPLE_4, standby = BME280.STANDBY_10, filter = BME280.FILTER_8)
    
    def get_temperature_celcius(self):
        """Read the temperature in celcius
        
        Returns the temperature in celcius"""
        return self.BME280.read_temperature()
    
    def get_temperature_fahrenheit(self):
        """Read the temperature in fahrenheit
        
        Returns the temperature in fahrenheit"""
        return (self.temperature_celcius() * ((9.0 / 5.0) + 32.0))
    
    def get_pressure(self):
        """Read the pressure in pascals
        
        Returns the pressure in pascals"""
        return self.BME280.read_pressure()
    
    def get_humidity(self):
        """Read the relative humidity in percentage
        
        Returns the relative humidity in percentage"""
        return self.BME280.read_humidity()
