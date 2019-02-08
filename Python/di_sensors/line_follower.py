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

    def __init__(self, bus = "RPI_1SW"):
        """Initialize the sensor

        Keyword arguments:
        bus (default "RPI_1SW") -- The I2C bus"""

        # create an I2C bus object and set the address
        self.i2c_bus = di_i2c.DI_I2C(bus = bus, address = 0x06)

    def read_sensors(self):
        """Read the Line Follower sensors"""

        array = self.i2c_bus.read_list(0x01, 8)
        for s in range(6):
            array[s] = (array[s] << 2) | ((array[6 + int(s / 4)] >> (2 * (s % 4))) & 0x03)
            array[s] = (1023 - array[s]) / 1023.0

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


class OldLineFollower(object):
    def __init__(self, bus = "RPI_1SW"):
        """Initialize the sensor

        Keyword arguments:
        bus (default "RPI_1SW") -- The I2C bus"""

        # create an I2C bus object and set the address
        self.i2c_bus = di_i2c.DI_I2C(bus = bus, address = 0x06)

    def read_sensors(self):
        """Read the Line Follower Sensors"""

        self.i2c_bus.write_reg_list(0x01, [0x03] + 3 * [0x00])
        time.sleep(0.01)
        self.i2c_bus.write_reg_list(0x01, [0x03] + 3 * [0x00])
        array = self.i2c_bus.read_list(None, 10)

        output = []
        for step in range(5):
            temp = array[2 * step] * 256 + array[2 * step + 1]
            output.append((1023 - temp) / 1023.0)

        return output
