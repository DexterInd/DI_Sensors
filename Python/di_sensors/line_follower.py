# https://www.dexterindustries.com
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# Python drivers for the Dexter Industries Line Follower sensor

from __future__ import print_function
from __future__ import division

from di_sensors import dexter_i2c
import time


class LineFollower(object):
    # reflected light mode
    REFLECTED = 1
    
    # LEDs in both active and inactive modes
    BOTH = 2
    
    # LEDs in active mode (reflected and ambient light)
    ACTIVE = 4
    
    # LEDs in inactive mode (ambient light)
    INACTIVE = 5
    
    def __init__(self, bus = "RPI_1"):
        """Initialize the sensor
        
        Keyword arguments:
        bus (default "RPI_1") -- The I2C bus"""
        
        # create an I2C bus object and set the address
        self.i2c_bus = dexter_i2c.Dexter_I2C(bus = bus, address = 0x06)
    
    def read_sensors(self, mode = REFLECTED):
        """Read the Line Follower sensors
        
        Keyword arguments:
        mode (default REFLECTED) -- The sensor mode. REFLECTED, BOTH, ACTIVE, or INACTIVE"""
        #self.i2c_bus.write_8(mode)
        ReadBytes = 8
        LSB_Offset = 6
        if mode == self.BOTH:
            ReadBytes = 15
            LSB_Offset = 12
        #if mode == self.REFLECTED or mode == self.BOTH:
        #    time.sleep(0.002)
        #else:
        #    time.sleep(0.0013)
        #array = self.i2c_bus.read_list(ReadBytes)
        
        array = self.i2c_bus.read_list(mode, ReadBytes)
        
        for g in range(3):
            for s in range(4):
                if mode == self.BOTH or not (g == 2 or (g == 1 and s > 1)):
                    temp = (array[(g * 4) + s] << 2) | ((array[LSB_Offset + g] >> (2 * s)) & 0x03)
                    array[(g * 4) + s] = (1023 - temp) / 1023.0
        return array[:LSB_Offset]
    
    def get_manufacturer(self):
        #self.i2c_bus.write_8(0x11)
        #array = self.i2c_bus.read_list(20)
        
        array = self.i2c_bus.read_list(0x11, 20)
        
        name = ""
        for c in range(20):
            if array[c] != 0:
                name += chr(array[c])
            else:
                break
        return name
    
    def get_board(self):
        #self.i2c_bus.write_8(0x12)
        #array = self.i2c_bus.read_list(20)
        
        array = self.i2c_bus.read_list(0x12, 20)
        
        name = ""
        for c in range(20):
            if array[c] != 0:
                name += chr(array[c])
            else:
                break
        return name
    
    def get_version_firmware(self):
        self.i2c_bus.write_8(0x13)
        return self.i2c_bus.read_32()
    
