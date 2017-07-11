# https://www.dexterindustries.com
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# Python drivers for the Dexter Industries Distance Sensor

from __future__ import print_function
from __future__ import division

from DI_Sensors import VL53L0X
import time


class DistanceSensor(object):
    """Drivers for the Dexter Industries Distance Sensor"""
    
    def __init__(self, bus = "RPI_1"):
        """Initialize the sensor
        
        Keyword arguments:
        bus (default "RPI_1") -- The I2C bus"""
        self.VL53L0X = VL53L0X.VL53L0X(bus = bus)
        
        # set to long range (about 2 meters)
        self.VL53L0X.set_signal_rate_limit(0.1)
        self.VL53L0X.set_vcsel_pulse_period(self.VL53L0X.VcselPeriodPreRange, 18)
        self.VL53L0X.set_vcsel_pulse_period(self.VL53L0X.VcselPeriodFinalRange, 14)
    
    def start_continuous(self, period_ms = 0):
        """Start taking continuous measurements
        
        Keyword arguments:
        period_ms (default 0) -- The time in ms between measurements"""
        self.VL53L0X.start_continuous(period_ms)
    
    def read_range_continuous(self):
        """Read range while taking continuous measurements
        
        Returns distance in mm"""
        return self.VL53L0X.read_range_continuous_millimeters()
    
    def read_range_single(self):
        """Read range with a single measurement
        
        Returns distance in mm"""
        return self.VL53L0X.read_range_single_millimeters()
    
    def timeout_occurred(self):
        """Check if timeout occured
        
        Returns True if timeout, otherwise False"""
        return self.VL53L0X.timeout_occurred()
