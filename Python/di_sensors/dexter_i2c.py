# https://www.dexterindustries.com
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# Python I2C drivers

from __future__ import print_function
from __future__ import division

import time


# Enabling one of the communication libraries
# This is not meant to change on a regular basis
# If Periphery doesn't work for you, uncomment either pigpio or smbus
#RPI_1_Module = "pigpio"
#RPI_1_Module = "smbus"
RPI_1_Module = "periphery"

if RPI_1_Module == "pigpio":
    import pigpio
elif RPI_1_Module == "smbus":
    import smbus
elif RPI_1_Module == "periphery":
    from periphery import I2C
else:
    raise IOError("RPI_1 module not supported")


class Dexter_I2C(object):
    """Dexter Industries I2C drivers for hardware and software I2C busses"""

    def __init__(self, bus, address, big_endian = True):
        """Initialize I2C

        Keyword arguments:
        bus -- The I2C bus. "RPI_1", "GPG3_AD1", or "GPG3_AD2".
        address -- the slave I2C address
        big_endian (default True) -- Big endian?"""
        if bus == "RPI_1":
            self.bus_name = bus

            if RPI_1_Module == "pigpio":
                self.i2c_bus = pigpio.pi()
                self.i2c_bus_handle = None
            elif RPI_1_Module == "smbus":
                self.i2c_bus = smbus.SMBus(1)
            elif RPI_1_Module == "periphery":
                self.bus_name = bus
                self.i2c_bus = I2C("/dev/i2c-1")
        elif bus == "GPG3_AD1" or bus == "GPG3_AD2":
            self.bus_name = bus

            self.gopigo3_module = __import__("gopigo3")
            self.gpg3 = self.gopigo3_module.GoPiGo3()
            if bus == "GPG3_AD1":
                self.port = self.gpg3.GROVE_1
            elif bus == "GPG3_AD2":
                self.port = self.gpg3.GROVE_2
            self.gpg3.set_grove_type(self.port, self.gpg3.GROVE_TYPE.I2C)
            time.sleep(0.01)
        elif bus == "BP3_1" or bus == "BP3_2" or bus == "BP3_3" or bus == "BP3_4":
            self.bus_name = bus

            self.brickpi3_module = __import__("brickpi3")
            self.bp3 = self.brickpi3_module.BrickPi3()
            if bus == "BP3_1":
                self.port = self.bp3.PORT_1
            elif bus == "BP3_2":
                self.port = self.bp3.PORT_2
            elif bus == "BP3_3":
                self.port = self.bp3.PORT_3
            elif bus == "BP3_4":
                self.port = self.bp3.PORT_4
            self.bp3.set_sensor_type(self.port, self.bp3.SENSOR_TYPE.I2C, [0, 0])
            time.sleep(0.01)
        else:
            raise IOError("I2C bus not supported")

        self.set_address(address)

        self.big_endian = big_endian

    def reconfig_bus(self):
        """Reconfigure I2C bus

        Reconfigure I2C port. If the port configuration got reset, call this method to reconfigure it."""
        if self.bus_name == "GPG3_AD1" or self.bus_name == "GPG3_AD2":
            self.gpg3.set_grove_type(self.port, self.gpg3.GROVE_TYPE.I2C)

    def set_address(self, address):
        """Set I2C address

        Keyword arguments:
        address -- the slave I2C address"""
        self.address = address
        if self.bus_name == "RPI_1" and RPI_1_Module == "pigpio":
            if self.i2c_bus_handle:
                self.i2c_bus.i2c_close(self.i2c_bus_handle)
            self.i2c_bus_handle = self.i2c_bus.i2c_open(1, address, 0)

    def transfer(self, outArr, inBytes = 0):
        """Conduct an I2C transfer (write and/or read)

        Keyword arguments:
        outArr -- list of bytes to write
        inBytes (default 0) -- how many bytes to read

        Returns list of bytes read"""
        if self.bus_name == "RPI_1":
            if RPI_1_Module == "pigpio":
                if(len(outArr) >= 2 and inBytes == 0):
                    self.i2c_bus.i2c_write_i2c_block_data(self.i2c_bus_handle, outArr[0], outArr[1:])
                elif(len(outArr) == 1 and inBytes == 0):
                    self.i2c_bus.i2c_write_byte(self.i2c_bus_handle, outArr[0])
                elif(len(outArr) == 1 and inBytes >= 1):
                    return self.i2c_bus.i2c_read_i2c_block_data(self.i2c_bus_handle, outArr[0], inBytes)
                elif(len(outArr) == 0 and inBytes >= 1):
                    return self.i2c_bus.i2c_read_byte(self.i2c_bus_handle)
                else:
                    raise IOError("I2C operation not supported")
            elif RPI_1_Module == "smbus":
                if(len(outArr) >= 2 and inBytes == 0):
                    self.i2c_bus.write_i2c_block_data(self.address, outArr[0], outArr[1:])
                elif(len(outArr) == 1 and inBytes == 0):
                    self.i2c_bus.write_byte(self.address, outArr[0])
                elif(len(outArr) == 1 and inBytes >= 1):
                    return self.i2c_bus.read_i2c_block_data(self.address, outArr[0], inBytes)
                elif(len(outArr) == 0 and inBytes == 1):
                    return self.i2c_bus.read_byte(self.address)
                else:
                    raise IOError("I2C operation not supported")
            elif RPI_1_Module == "periphery":
                msgs = []
                offset = 0
                if(len(outArr) > 0):
                    msgs.append(self.i2c_bus.Message(outArr))
                    offset = 1
                if(inBytes):
                    r = [0 for b in range(inBytes)]
                    msgs.append(self.i2c_bus.Message(r, read = True))
                if(len(msgs) >= 1):
                    self.i2c_bus.transfer(self.address, msgs)
                if(inBytes):
                    return msgs[offset].data
                return

        elif self.bus_name == "GPG3_AD1" or self.bus_name == "GPG3_AD2":
            try:
                return self.gpg3.grove_i2c_transfer(self.port, self.address, outArr, inBytes)
            except self.gopigo3_module.I2CError:
                raise IOError("[Errno 5] Input/output error")

        elif self.bus_name == "BP3_1" or self.bus_name == "BP3_2" or self.bus_name == "BP3_3" or self.bus_name == "BP3_4":
            try:
                return self.bp3.i2c_transfer(self.port, self.address, outArr, inBytes)
            except self.brickpi3_module.I2CError:
                raise IOError("[Errno 5] Input/output error")

    def write_8(self, val):
        """Write an 8-bit value

        Keyword arguments:
        val -- byte to write"""
        val = int(val)
        self.transfer([val])

    def write_reg_8(self, reg, val):
        """Write an 8-bit value to a register

        Keyword arguments:
        reg -- register to write to
        val -- byte to write"""
        val = int(val)
        self.transfer([reg, val])

    def write_reg_16(self, reg, val, big_endian = None):
        """Write a 16-bit value to a register

        Keyword arguments:
        reg -- register to write to
        val -- data to write
        big_endian (default None) -- True (big endian), False (little endian), or None (use the pre-defined endianness for the object)"""
        val = int(val)
        if big_endian == None:
            big_endian = self.big_endian
        if big_endian:
            self.transfer([reg, ((val >> 8) & 0xFF), (val & 0xFF)])
        else:
            self.transfer([reg, (val & 0xFF), ((val >> 8) & 0xFF)])

    def write_reg_32(self, reg, val, big_endian = None):
        """Write a 32-bit value to a register

        Keyword arguments:
        reg -- register to write to
        val -- data to write
        big_endian (default None) -- True (big endian), False (little endian), or None (use the pre-defined endianness for the object)"""
        val = int(val)
        if big_endian == None:
            big_endian = self.big_endian
        if big_endian:
            self.transfer( [reg, ((val >> 24) & 0xFF), ((val >> 16) & 0xFF), ((val >> 8) & 0xFF), (val & 0xFF)])
        else:
            self.transfer([reg, (val & 0xFF), ((val >> 8) & 0xFF), ((val >> 16) & 0xFF), ((val >> 24) & 0xFF)])

    def write_reg_list(self, reg, list):
        """Write a list of bytes to a register

        Keyword arguments:
        reg -- regester to write to
        list -- list of bytes to write"""
        arr = [reg]
        arr.extend(list)
        self.transfer(arr)

    def read_8u(self):
        """Read an 8-bit value

        Returns the value"""
        val = self.transfer([], 1)
        return val

    def read_reg_8u(self, reg):
        """Read an 8-bit unsigned value from a register

        Keyword arguments:
        reg -- regester to read from

        Returns the value
        """
        val = self.transfer([reg], 1)
        return val[0]

    def read_reg_8s(self, reg):
        """Read an 8-bit signed value from a register

        Keyword arguments:
        reg -- regester to read from

        Returns the value
        """
        val = self.read_reg_8u(reg)
        if val & 0x80:
            return val - 0x100
        return val

    def read_reg_16u(self, reg, big_endian = None):
        """Read a 16-bit unsigned value from a register

        Keyword arguments:
        reg -- regester to read from
        big_endian (default None) -- True (big endian), False (little endian), or None (use the pre-defined endianness for the object)

        Returns the value
        """
        val = self.transfer([reg], 2)
        if big_endian == None:
            big_endian = self.big_endian
        if big_endian:
            return (val[0] << 8) | val[1]
        else:
            return (val[1] << 8) | val[0]

    def read_reg_16s(self, reg, big_endian = None):
        """Read a 16-bit signed value from a register

        Keyword arguments:
        reg -- regester to read from
        big_endian (default None) -- True (big endian), False (little endian), or None (use the pre-defined endianness for the object)

        Returns the value
        """
        val = self.read_reg_16u(reg, big_endian)
        if val & 0x8000:
            return val - 0x10000
        return val

    def read_32u(self, big_endian = None):
        """Read a 32-bit unsigned value

        Keyword arguments:
        big_endian (default None) -- True (big endian), False (little endian), or None (use the pre-defined endianness for the object)

        Returns the value
        """
        val = self.transfer([], 4)
        if big_endian == None:
            big_endian = self.big_endian
        if big_endian:
            return (val[0] << 24) | (val[1] << 16) | (val[2] << 8) | val[3]
        else:
            return (val[3] << 24) | (val[2] << 16) | (val[1] << 8) | val[0]

    def read_list(self, len):
        """Read a list of bytes

        Keyword arguments:
        len -- the number of bytes to read

        Returns a list of the bytes read"""
        return self.transfer([], len)

    def read_reg_list(self, reg, len):
        """Read a list of bytes from a register

        Keyword arguments:
        reg -- the regester to read from
        len -- the number of bytes to read

        Returns a list of the bytes read"""
        return self.transfer([reg], len)
