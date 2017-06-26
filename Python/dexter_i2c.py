# https://www.dexterindustries.com
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# Python I2C drivers


class Dexter_I2C():
    """Dexter Industries I2C drivers for hardware and software I2C busses"""
    
    def __init__(self, bus, big_endian = True):
        """Initialize I2C
        
        Keyword arguments:
        bus (default "RPI_1") -- The I2C bus. "RPI_1", "GPG3_AD1", or "GPG3_AD2".
        big_endian (default True) -- Big endian?"""
        if bus == "RPI_1":
            import smbus
            self.i2c_bus = smbus.SMBus(1)
        elif bus == "GPG3_AD1" or bus == "GPG3_AD2":
            import gopigo3
            self.gpg3 = gopigo3.GoPiGo3()
            if bus == "GPG3_AD1":
                self.port = self.gpg3.GROVE_1
            elif bus == "GPG3_AD2":
                self.port = self.gpg3.GROVE_2
            self.gpg3.set_grove_type(self.port, self.gpg3.GROVE_TYPE.I2C)
        else:
            raise IOError("I2C bus not supported")
        
        self.bus_name = bus
        self.big_endian = big_endian
    
    def set_address(self, addr):
        """Set I2C address
        
        Keyword arguments:
        addr -- the slave I2C address"""
        self.addr = addr
    
    def transfer(self, outArr, inBytes = 0):
        """Conduct an I2C transfer (write and/or read)
        
        Keyword arguments:
        outArr -- list of bytes to write
        inBytes (default 0) -- how many bytes to read
        
        Returns list of bytes read"""
        if self.bus_name == "RPI_1":
            #if(len(outArr) == 2 and inBytes == 0):
            #    self.i2c_bus.write_byte_data(addr, outArr[0], outArr[1])
            #elif(len(outArr) > 2 and inBytes == 0):
            if(len(outArr) >= 2 and inBytes == 0):
                self.i2c_bus.write_i2c_block_data(self.addr, outArr[0], outArr[1:])
            elif(len(outArr) == 1 and inBytes == 0):
                self.i2c_bus.write_byte(self.addr, outArr[0])
            #elif(len(outArr) == 1 and inBytes == 1):
            #    return self.i2c_bus.read_byte_data(self.addr, outArr[0]) & 0xFF
            #elif(len(outArr) == 1 and inBytes > 1):
            elif(len(outArr) == 1 and inBytes >= 1):
                return self.i2c_bus.read_i2c_block_data(self.addr, outArr[0], inBytes)
            elif(len(outArr) == 0 and inBytes >= 1):
                return self.i2c_bus.read_byte(self.addr)
            else:
                raise IOError("I2C operation not supported")
            
        elif self.bus_name == "GPG3_AD1" or self.bus_name == "GPG3_AD2":
            try:
                return self.gpg3.grove_i2c_transfer(self.port, self.addr, outArr, inBytes)
            except gopigo3.I2CError:
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
    
    def read_reg_list(self, reg, len):
        """Read a list of bytes from a register
        
        Keyword arguments:
        reg -- the regester to read from
        len -- the number of bytes to read
        
        Returns a list of the bytes read"""
        return self.transfer([reg], len)
