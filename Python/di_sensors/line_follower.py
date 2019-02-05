# https://www.dexterindustries.com
#
# Copyright (c) 2019 Dexter Industries
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
        self.board = self.detect_line_follower()

    def detect_line_follower(self):
        """
        returns
        0 - for no line follower detected
        1 - for detecting the old line follower
        2 - for detecting the new line follower
        """
        # see if the device is up and running
        counter = 0
        device_on = False
        max_retries = 3
        while counter < max_retries:
            try:
                self.i2c_bus.read_8()
                device_on = True
                break
            except:
                counter += 1
        
        if device_on is True:
            # then it means we have a line follower connected
            # we still don't know whether it is the new one or the old one
            counter = 0
            board = 1
            # check if we can call a method specific to the new line follower
            while counter < max_retries:
                try:
                    self.get_board()
                    board = 2
                    break
                except:
                    counter += 1
            return board
        else:
            return 0
    
    def read_sensors(self, mode = REFLECTED):
        """Read the Line Follower sensors
        
        Keyword arguments:
        mode (default REFLECTED) -- The sensor mode. REFLECTED, BOTH, ACTIVE, or INACTIVE"""

        if self.board == 2:
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

            array = array[:LSB_Offset]
            array = array[::-1]
            return array
        elif self.board == 1:
            # the old line follower has to be issued the read command
            # twice in order for the current values to be returned
            self.i2c_bus.write_reg_list(0x01, [0x03] + 3 * [0x00])
            time.sleep(0.01)
            self.i2c_bus.write_reg_list(0x01, [0x03] + 3 * [0x00])
            array = self.i2c_bus.read_list(None, 10)

            output = []
            for step in range(5):
                temp = array[2 * step] * 256 + array[2 * step + 1]
                output.append((1023 - temp) / 1023.0)
            return output[::-1]
    
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
    
