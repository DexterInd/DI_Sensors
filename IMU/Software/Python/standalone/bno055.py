import time
import smbus

# I2C addresses
BNO055_ADDRESS_A                     = 0x28
BNO055_ADDRESS_B                     = 0x29
BNO055_ID                            = 0xA0

# Page id register definition
BNO055_PAGE_ID_ADDR                  = 0X07

# PAGE0 REGISTER DEFINITION START
BNO055_CHIP_ID_ADDR                  = 0x00
BNO055_ACCEL_REV_ID_ADDR             = 0x01
BNO055_MAG_REV_ID_ADDR               = 0x02
BNO055_GYRO_REV_ID_ADDR              = 0x03
BNO055_SW_REV_ID_LSB_ADDR            = 0x04
BNO055_SW_REV_ID_MSB_ADDR            = 0x05
BNO055_BL_REV_ID_ADDR                = 0X06

# Accel data register
BNO055_ACCEL_DATA_X_LSB_ADDR         = 0X08
BNO055_ACCEL_DATA_X_MSB_ADDR         = 0X09
BNO055_ACCEL_DATA_Y_LSB_ADDR         = 0X0A
BNO055_ACCEL_DATA_Y_MSB_ADDR         = 0X0B
BNO055_ACCEL_DATA_Z_LSB_ADDR         = 0X0C
BNO055_ACCEL_DATA_Z_MSB_ADDR         = 0X0D

# Mag data register
BNO055_MAG_DATA_X_LSB_ADDR           = 0X0E
BNO055_MAG_DATA_X_MSB_ADDR           = 0X0F
BNO055_MAG_DATA_Y_LSB_ADDR           = 0X10
BNO055_MAG_DATA_Y_MSB_ADDR           = 0X11
BNO055_MAG_DATA_Z_LSB_ADDR           = 0X12
BNO055_MAG_DATA_Z_MSB_ADDR           = 0X13

# Gyro data registers
BNO055_GYRO_DATA_X_LSB_ADDR          = 0X14
BNO055_GYRO_DATA_X_MSB_ADDR          = 0X15
BNO055_GYRO_DATA_Y_LSB_ADDR          = 0X16
BNO055_GYRO_DATA_Y_MSB_ADDR          = 0X17
BNO055_GYRO_DATA_Z_LSB_ADDR          = 0X18
BNO055_GYRO_DATA_Z_MSB_ADDR          = 0X19

# Euler data registers
BNO055_EULER_H_LSB_ADDR              = 0X1A
BNO055_EULER_H_MSB_ADDR              = 0X1B
BNO055_EULER_R_LSB_ADDR              = 0X1C
BNO055_EULER_R_MSB_ADDR              = 0X1D
BNO055_EULER_P_LSB_ADDR              = 0X1E
BNO055_EULER_P_MSB_ADDR              = 0X1F

# Quaternion data registers
BNO055_QUATERNION_DATA_W_LSB_ADDR    = 0X20
BNO055_QUATERNION_DATA_W_MSB_ADDR    = 0X21
BNO055_QUATERNION_DATA_X_LSB_ADDR    = 0X22
BNO055_QUATERNION_DATA_X_MSB_ADDR    = 0X23
BNO055_QUATERNION_DATA_Y_LSB_ADDR    = 0X24
BNO055_QUATERNION_DATA_Y_MSB_ADDR    = 0X25
BNO055_QUATERNION_DATA_Z_LSB_ADDR    = 0X26
BNO055_QUATERNION_DATA_Z_MSB_ADDR    = 0X27

# Linear acceleration data registers
BNO055_LINEAR_ACCEL_DATA_X_LSB_ADDR  = 0X28
BNO055_LINEAR_ACCEL_DATA_X_MSB_ADDR  = 0X29
BNO055_LINEAR_ACCEL_DATA_Y_LSB_ADDR  = 0X2A
BNO055_LINEAR_ACCEL_DATA_Y_MSB_ADDR  = 0X2B
BNO055_LINEAR_ACCEL_DATA_Z_LSB_ADDR  = 0X2C
BNO055_LINEAR_ACCEL_DATA_Z_MSB_ADDR  = 0X2D

# Gravity data registers
BNO055_GRAVITY_DATA_X_LSB_ADDR       = 0X2E
BNO055_GRAVITY_DATA_X_MSB_ADDR       = 0X2F
BNO055_GRAVITY_DATA_Y_LSB_ADDR       = 0X30
BNO055_GRAVITY_DATA_Y_MSB_ADDR       = 0X31
BNO055_GRAVITY_DATA_Z_LSB_ADDR       = 0X32
BNO055_GRAVITY_DATA_Z_MSB_ADDR       = 0X33

# Temperature data register
BNO055_TEMP_ADDR                     = 0X34

# Status registers
BNO055_CALIB_STAT_ADDR               = 0X35
BNO055_SELFTEST_RESULT_ADDR          = 0X36
BNO055_INTR_STAT_ADDR                = 0X37

BNO055_SYS_CLK_STAT_ADDR             = 0X38
BNO055_SYS_STAT_ADDR                 = 0X39
BNO055_SYS_ERR_ADDR                  = 0X3A

# Unit selection register
BNO055_UNIT_SEL_ADDR                 = 0X3B
BNO055_DATA_SELECT_ADDR              = 0X3C

# Mode registers
BNO055_OPR_MODE_ADDR                 = 0X3D
BNO055_PWR_MODE_ADDR                 = 0X3E

BNO055_SYS_TRIGGER_ADDR              = 0X3F
BNO055_TEMP_SOURCE_ADDR              = 0X40

# Axis remap registers
BNO055_AXIS_MAP_CONFIG_ADDR          = 0X41
BNO055_AXIS_MAP_SIGN_ADDR            = 0X42

# Axis remap values
AXIS_REMAP_X                         = 0x00
AXIS_REMAP_Y                         = 0x01
AXIS_REMAP_Z                         = 0x02
AXIS_REMAP_POSITIVE                  = 0x00
AXIS_REMAP_NEGATIVE                  = 0x01

# SIC registers
BNO055_SIC_MATRIX_0_LSB_ADDR         = 0X43
BNO055_SIC_MATRIX_0_MSB_ADDR         = 0X44
BNO055_SIC_MATRIX_1_LSB_ADDR         = 0X45
BNO055_SIC_MATRIX_1_MSB_ADDR         = 0X46
BNO055_SIC_MATRIX_2_LSB_ADDR         = 0X47
BNO055_SIC_MATRIX_2_MSB_ADDR         = 0X48
BNO055_SIC_MATRIX_3_LSB_ADDR         = 0X49
BNO055_SIC_MATRIX_3_MSB_ADDR         = 0X4A
BNO055_SIC_MATRIX_4_LSB_ADDR         = 0X4B
BNO055_SIC_MATRIX_4_MSB_ADDR         = 0X4C
BNO055_SIC_MATRIX_5_LSB_ADDR         = 0X4D
BNO055_SIC_MATRIX_5_MSB_ADDR         = 0X4E
BNO055_SIC_MATRIX_6_LSB_ADDR         = 0X4F
BNO055_SIC_MATRIX_6_MSB_ADDR         = 0X50
BNO055_SIC_MATRIX_7_LSB_ADDR         = 0X51
BNO055_SIC_MATRIX_7_MSB_ADDR         = 0X52
BNO055_SIC_MATRIX_8_LSB_ADDR         = 0X53
BNO055_SIC_MATRIX_8_MSB_ADDR         = 0X54

# Accelerometer Offset registers
ACCEL_OFFSET_X_LSB_ADDR              = 0X55
ACCEL_OFFSET_X_MSB_ADDR              = 0X56
ACCEL_OFFSET_Y_LSB_ADDR              = 0X57
ACCEL_OFFSET_Y_MSB_ADDR              = 0X58
ACCEL_OFFSET_Z_LSB_ADDR              = 0X59
ACCEL_OFFSET_Z_MSB_ADDR              = 0X5A

# Magnetometer Offset registers
MAG_OFFSET_X_LSB_ADDR                = 0X5B
MAG_OFFSET_X_MSB_ADDR                = 0X5C
MAG_OFFSET_Y_LSB_ADDR                = 0X5D
MAG_OFFSET_Y_MSB_ADDR                = 0X5E
MAG_OFFSET_Z_LSB_ADDR                = 0X5F
MAG_OFFSET_Z_MSB_ADDR                = 0X60

# Gyroscope Offset register s
GYRO_OFFSET_X_LSB_ADDR               = 0X61
GYRO_OFFSET_X_MSB_ADDR               = 0X62
GYRO_OFFSET_Y_LSB_ADDR               = 0X63
GYRO_OFFSET_Y_MSB_ADDR               = 0X64
GYRO_OFFSET_Z_LSB_ADDR               = 0X65
GYRO_OFFSET_Z_MSB_ADDR               = 0X66

# Radius registers
ACCEL_RADIUS_LSB_ADDR                = 0X67
ACCEL_RADIUS_MSB_ADDR                = 0X68
MAG_RADIUS_LSB_ADDR                  = 0X69
MAG_RADIUS_MSB_ADDR                  = 0X6A

# Power modes
POWER_MODE_NORMAL                    = 0X00
POWER_MODE_LOWPOWER                  = 0X01
POWER_MODE_SUSPEND                   = 0X02

# Operation mode settings
OPERATION_MODE_CONFIG                = 0X00
OPERATION_MODE_ACCONLY               = 0X01
OPERATION_MODE_MAGONLY               = 0X02
OPERATION_MODE_GYRONLY               = 0X03
OPERATION_MODE_ACCMAG                = 0X04
OPERATION_MODE_ACCGYRO               = 0X05
OPERATION_MODE_MAGGYRO               = 0X06
OPERATION_MODE_AMG                   = 0X07
OPERATION_MODE_IMUPLUS               = 0X08
OPERATION_MODE_COMPASS               = 0X09
OPERATION_MODE_M4G                   = 0X0A
OPERATION_MODE_NDOF_FMC_OFF          = 0X0B
OPERATION_MODE_NDOF                  = 0X0C

class BNO055(object):
    
    def __init__(self, address=BNO055_ADDRESS_A):
        self.bus = smbus.SMBus(1)
        self._address = 0x28
        
    def _write_bytes(self, register, data):
        # Write a list of 8-bit values starting at the provided register 
        # self._i2c_device.writeList(address, data)
        self._bus.write_i2c_block_data(self._address, register, data)
        
    def _write_byte(self, register, value, ack=True):
        self.bus.write_byte_data(self._address, register, value)
        # self._i2c_device.write8(address, value)
        
    def _read_bytes(self, register, length):
        # return bytearray(self._i2c_device.readList(address, length))
        results = self.bus.read_i2c_block_data(self._address, register, length)
        return bytearray(results)
   
    def _read_byte(self, register):
        return self.bus.read_byte_data(self._address, register) & 0xFF
        
    def _read_signed_byte(self, address):
        # Read an 8-bit signed value from the provided register address.
        data = self._read_byte(address)
        if data > 127:
            return data - 256
        else:
            return data
    
    def set_mode(self, mode):
        """Set operation mode for BNO055 sensor.  Mode should be a value from
        table 3-3 and 3-5 of the datasheet:
          http://www.adafruit.com/datasheets/BST_BNO055_DS000_12.pdf
        """
        self._write_byte(BNO055_OPR_MODE_ADDR, mode & 0xFF)
        # Delay for 30 milliseconds (datsheet recommends 19ms, but a little more
        # can't hurt and the kernel is going to spend some unknown amount of time
        # too).
        time.sleep(0.03)
        
    def _config_mode(self):
        # Enter configuration mode.
        self.set_mode(OPERATION_MODE_CONFIG)

    def _operation_mode(self):
        # Enter operation mode to read sensor data.
        self.set_mode(self._mode)
        
    def begin(self, mode=OPERATION_MODE_NDOF):
        self._mode = mode
        try:
            self._write_byte(BNO055_PAGE_ID_ADDR, 0, ack=False)
        except IOError:
            # Swallow an IOError that might be raised by an I2C issue.  Only do
            # this for this very first command to help get the BNO and board's
            # I2C into a clear state ready to accept the next commands.
            pass
        self._config_mode()
        self._write_byte(BNO055_PAGE_ID_ADDR, 0)
        # Check the chip ID
        bno_id = self._read_byte(BNO055_CHIP_ID_ADDR)
        # logger.debug('Read chip ID: 0x{0:02X}'.format(bno_id))
        if bno_id != BNO055_ID:
            return False
            
        self._write_byte(BNO055_SYS_TRIGGER_ADDR, 0x20, ack=False)
        # Wait 650ms after reset for chip to be ready (as suggested
        # in datasheet).
        time.sleep(0.65)
        # Set to normal power mode.
        self._write_byte(BNO055_PWR_MODE_ADDR, POWER_MODE_NORMAL)
        # Default to internal oscillator.
        self._write_byte(BNO055_SYS_TRIGGER_ADDR, 0x80)
        # Enter normal operation mode.
        self._operation_mode()
        return True
        
    def get_system_status(self, run_self_test=True):
        """Return a tuple with status information.  Three values will be returned:
          - System status register value with the following meaning:
              0 = Idle
              1 = System Error
              2 = Initializing Peripherals
              3 = System Initialization
              4 = Executing Self-Test
              5 = Sensor fusion algorithm running
              6 = System running without fusion algorithms
          - Self test result register value with the following meaning:
              Bit value: 1 = test passed, 0 = test failed
              Bit 0 = Accelerometer self test
              Bit 1 = Magnetometer self test
              Bit 2 = Gyroscope self test
              Bit 3 = MCU self test
              Value of 0x0F = all good!
          - System error register value with the following meaning:
              0 = No error
              1 = Peripheral initialization error
              2 = System initialization error
              3 = Self test result failed
              4 = Register map value out of range
              5 = Register map address out of range
              6 = Register map write error
              7 = BNO low power mode not available for selected operation mode
              8 = Accelerometer power mode not available
              9 = Fusion algorithm configuration error
             10 = Sensor configuration error

        If run_self_test is passed in as False then no self test is performed and
        None will be returned for the self test result.  Note that running a
        self test requires going into config mode which will stop the fusion
        engine from running.
        """
        self_test = None
        if run_self_test:
            # Switch to configuration mode if running self test.
            self._config_mode()
            # Perform a self test.
            sys_trigger = self._read_byte(BNO055_SYS_TRIGGER_ADDR)
            self._write_byte(BNO055_SYS_TRIGGER_ADDR, sys_trigger | 0x1)
            # Wait for self test to finish.
            time.sleep(1.0)
            # Read test result.
            self_test = self._read_byte(BNO055_SELFTEST_RESULT_ADDR)
            # Go back to operation mode.
            self._operation_mode()
        # Now read status and error registers.
        status = self._read_byte(BNO055_SYS_STAT_ADDR)
        error = self._read_byte(BNO055_SYS_ERR_ADDR)
        # Return the results as a tuple of all 3 values.
        return (status, self_test, error)
        
    def get_revision(self):
        """Return a tuple with revision information about the BNO055 chip.  Will
        return 5 values:
          - Software revision
          - Bootloader version
          - Accelerometer ID
          - Magnetometer ID
          - Gyro ID
        """
        # Read revision values.
        accel = self._read_byte(BNO055_ACCEL_REV_ID_ADDR)
        mag = self._read_byte(BNO055_MAG_REV_ID_ADDR)
        gyro = self._read_byte(BNO055_GYRO_REV_ID_ADDR)
        bl = self._read_byte(BNO055_BL_REV_ID_ADDR)
        sw_lsb = self._read_byte(BNO055_SW_REV_ID_LSB_ADDR)
        sw_msb = self._read_byte(BNO055_SW_REV_ID_MSB_ADDR)
        sw = ((sw_msb << 8) | sw_lsb) & 0xFFFF
        # Return the results as a tuple of all 5 values.
        return (sw, bl, accel, mag, gyro)
        
    def read_euler(self):
        """Return the current absolute orientation as a tuple of heading, roll,
        and pitch euler angles in degrees.
        """
        heading, roll, pitch = self._read_vector(BNO055_EULER_H_LSB_ADDR)
        return (heading/16.0, roll/16.0, pitch/16.0)
        
    def _read_vector(self, address, count=3):
        # Read count number of 16-bit signed values starting from the provided
        # address. Returns a tuple of the values that were read.
        
        # data = self._read_bytes(address, count*2)
        # for i in range(len(data)):
            # print int(data[i])
        result = [0]*count
        
        # reg1_data=self._i2c_device.readU16(reg1_addr)
        # reg2_data=self._i2c_device.readU16(reg2_addr)
        # reg3_data=self._i2c_device.readU16(reg3_addr)
        
        # print reg1_data%255,reg1_data/255,reg1_data
        # print reg2_data%255,reg2_data/255,reg2_data
        # print reg3_data%255,reg3_data/255,reg3_data
        data =[]
        for i in range(count*2):
            # data.append(self._i2c_device.readU8(address+i))
            data.append(self.bus.read_byte_data(self._address, address+i) & 0xFF)

        for i in range(count):
            # print int(data[i*2+1]),int(data[i*2]),((data[i*2+1] << 8) | data[i*2]) & 0xFFFF
            result[i] = ((data[i*2+1] << 8) | data[i*2]) & 0xFFFF
            if result[i] > 32767:
                result[i] -= 65536
        return result
        # return [0,0,0]
        
    # def _read_vector(self, address, count=3):
        # # Read count number of 16-bit signed values starting from the provided
        # # address. Returns a tuple of the values that were read.
        # data = self._read_bytes(address, 6)
        # for i in range(len(data)):
            # print int(data[i])
        # result = [0]*count
        
        # for i in range(count):
            # print int(data[i*2+1]),int(data[i*2]),((data[i*2+1] << 8) | data[i*2]) & 0xFFFF
            # result[i] = ((data[i*2+1] << 8) | data[i*2]) & 0xFFFF
            # if result[i] > 32767:
                # result[i] -= 65536
        # return result