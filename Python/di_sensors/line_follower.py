# https://www.dexterindustries.com
#
# Copyright (c) 2019 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# Python drivers for the Dexter Industries Line Follower sensor

from __future__ import print_function
from __future__ import division

import di_i2c
import time


class LineFollower(object):

    def __init__(self, bus = "RPI_1"):
        """Initialize the sensor

        Keyword arguments:
        bus (default "RPI_1") -- The I2C bus"""

        # create an I2C bus object and set the address
        self.i2c_bus = dexter_i2c.Dexter_I2C(bus = bus, address = 0x06)

    def read_sensors(self):
        """Read the Line Follower sensors"""

        array = self.i2c_bus.read_list(0x01, 8)
        for s in range(6):
            array[s] = (array[s] << 2) | ((array[6 + int(s / 4)] >> (2 * (s % 4))) & 0x03)

        return array[:6]

    def get_manufacturer(self):
        """Read the manufacturer name"""

        array = self.i2c_bus.read_list(0x11, 20)

        name = ""
        for c in range(20):
            if array[c] != 0:
                name += chr(array[c])
            else:
                break
        return name

    def get_board(self):
        """Read the board name"""

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
