// https://www.dexterindustries.com/GoPiGo/
// https://github.com/DexterInd/DI_Sensors
//
// Copyright (c) 2017 Dexter Industries
// Released under the MIT license (http://choosealicense.com/licenses/mit/).
// For more information see https://github.com/DexterInd/GoPiGo3/blob/master/LICENSE.md

const Sensor = require('./base/sensor');

class BNO055 extends Sensor {
    // I2C addresses
    static ADDRESS_A                   = 0x28;
    static ADDRESS_B                   = 0x29;

    static ID                          = 0xA0;

    // Page id register definition
    static REG_PAGE_ID                 = 0x07;

    // PAGE0 REGISTER DEFINITION START
    static REG_CHIP_ID                 = 0x00;
    static REG_ACCEL_REV_ID            = 0x01;
    static REG_MAG_REV_ID              = 0x02;
    static REG_GYRO_REV_ID             = 0x03;
    static REG_SW_REV_ID_LSB           = 0x04;
    static REG_SW_REV_ID_MSB           = 0x05;
    static REG_BL_REV_ID               = 0x06;

    // Accel data register
    static REG_ACCEL_DATA_X_LSB        = 0x08;
    static REG_ACCEL_DATA_X_MSB        = 0x09;
    static REG_ACCEL_DATA_Y_LSB        = 0x0A;
    static REG_ACCEL_DATA_Y_MSB        = 0x0B;
    static REG_ACCEL_DATA_Z_LSB        = 0x0C;
    static REG_ACCEL_DATA_Z_MSB        = 0x0D;

    // Mag data register
    static REG_MAG_DATA_X_LSB          = 0x0E;
    static REG_MAG_DATA_X_MSB          = 0x0F;
    static REG_MAG_DATA_Y_LSB          = 0x10;
    static REG_MAG_DATA_Y_MSB          = 0x11;
    static REG_MAG_DATA_Z_LSB          = 0x12;
    static REG_MAG_DATA_Z_MSB          = 0x13;

    // Gyro data registers
    static REG_GYRO_DATA_X_LSB         = 0x14;
    static REG_GYRO_DATA_X_MSB         = 0x15;
    static REG_GYRO_DATA_Y_LSB         = 0x16;
    static REG_GYRO_DATA_Y_MSB         = 0x17;
    static REG_GYRO_DATA_Z_LSB         = 0x18;
    static REG_GYRO_DATA_Z_MSB         = 0x19;

    // Euler data registers
    static REG_EULER_H_LSB             = 0x1A;
    static REG_EULER_H_MSB             = 0x1B;
    static REG_EULER_R_LSB             = 0x1C;
    static REG_EULER_R_MSB             = 0x1D;
    static REG_EULER_P_LSB             = 0x1E;
    static REG_EULER_P_MSB             = 0x1F;

    // Quaternion data registers
    static REG_QUATERNION_DATA_W_LSB   = 0x20;
    static REG_QUATERNION_DATA_W_MSB   = 0x21;
    static REG_QUATERNION_DATA_X_LSB   = 0x22;
    static REG_QUATERNION_DATA_X_MSB   = 0x23;
    static REG_QUATERNION_DATA_Y_LSB   = 0x24;
    static REG_QUATERNION_DATA_Y_MSB   = 0x25;
    static REG_QUATERNION_DATA_Z_LSB   = 0x26;
    static REG_QUATERNION_DATA_Z_MSB   = 0x27;

    // Linear acceleration data registers
    static REG_LINEAR_ACCEL_DATA_X_LSB = 0x28;
    static REG_LINEAR_ACCEL_DATA_X_MSB = 0x29;
    static REG_LINEAR_ACCEL_DATA_Y_LSB = 0x2A;
    static REG_LINEAR_ACCEL_DATA_Y_MSB = 0x2B;
    static REG_LINEAR_ACCEL_DATA_Z_LSB = 0x2C;
    static REG_LINEAR_ACCEL_DATA_Z_MSB = 0x2D;

    // Gravity data registers
    static REG_GRAVITY_DATA_X_LSB      = 0x2E;
    static REG_GRAVITY_DATA_X_MSB      = 0x2F;
    static REG_GRAVITY_DATA_Y_LSB      = 0x30;
    static REG_GRAVITY_DATA_Y_MSB      = 0x31;
    static REG_GRAVITY_DATA_Z_LSB      = 0x32;
    static REG_GRAVITY_DATA_Z_MSB      = 0x33;

    // Temperature data register
    static REG_TEMP                    = 0x34;

    // Status registers
    static REG_CALIB_STAT              = 0x35;
    static REG_SELFTEST_RESULT         = 0x36;
    static REG_INTR_STAT               = 0x37;

    static REG_SYS_CLK_STAT            = 0x38;
    static REG_SYS_STAT                = 0x39;
    static REG_SYS_ERR                 = 0x3A;

    // Unit selection register
    static REG_UNIT_SEL                = 0x3B;
    static UNIT_SEL_ACC  = 0x01;
    static UNIT_SEL_GYR  = 0x02;
    static UNIT_SEL_EUL  = 0x04;
    static UNIT_SEL_TEMP = 0x10;
    static UNIT_SEL_ORI  = 0x80;

    static REG_DATA_SELECT             = 0x3C;

    // Mode registers
    static REG_OPR_MODE                = 0x3D;
    static REG_PWR_MODE                = 0x3E;

    static REG_SYS_TRIGGER             = 0x3F;
    static REG_TEMP_SOURCE             = 0x40;

    // Axis remap registers
    static REG_AXIS_MAP_CONFIG         = 0x41;
    static REG_AXIS_MAP_SIGN           = 0x42;

    // Axis remap values
    static AXIS_REMAP_X                = 0x00;
    static AXIS_REMAP_Y                = 0x01;
    static AXIS_REMAP_Z                = 0x02;
    static AXIS_REMAP_POSITIVE         = 0x00;
    static AXIS_REMAP_NEGATIVE         = 0x01;

    // SIC registers
    static REG_SIC_MATRIX_0_LSB        = 0x43;
    static REG_SIC_MATRIX_0_MSB        = 0x44;
    static REG_SIC_MATRIX_1_LSB        = 0x45;
    static REG_SIC_MATRIX_1_MSB        = 0x46;
    static REG_SIC_MATRIX_2_LSB        = 0x47;
    static REG_SIC_MATRIX_2_MSB        = 0x48;
    static REG_SIC_MATRIX_3_LSB        = 0x49;
    static REG_SIC_MATRIX_3_MSB        = 0x4A;
    static REG_SIC_MATRIX_4_LSB        = 0x4B;
    static REG_SIC_MATRIX_4_MSB        = 0x4C;
    static REG_SIC_MATRIX_5_LSB        = 0x4D;
    static REG_SIC_MATRIX_5_MSB        = 0x4E;
    static REG_SIC_MATRIX_6_LSB        = 0x4F;
    static REG_SIC_MATRIX_6_MSB        = 0x50;
    static REG_SIC_MATRIX_7_LSB        = 0x51;
    static REG_SIC_MATRIX_7_MSB        = 0x52;
    static REG_SIC_MATRIX_8_LSB        = 0x53;
    static REG_SIC_MATRIX_8_MSB        = 0x54;

    // Accelerometer Offset registers
    static REG_ACCEL_OFFSET_X_LSB      = 0x55;
    static REG_ACCEL_OFFSET_X_MSB      = 0x56;
    static REG_ACCEL_OFFSET_Y_LSB      = 0x57;
    static REG_ACCEL_OFFSET_Y_MSB      = 0x58;
    static REG_ACCEL_OFFSET_Z_LSB      = 0x59;
    static REG_ACCEL_OFFSET_Z_MSB      = 0x5A;

    // Magnetometer Offset registers
    static REG_MAG_OFFSET_X_LSB        = 0x5B;
    static REG_MAG_OFFSET_X_MSB        = 0x5C;
    static REG_MAG_OFFSET_Y_LSB        = 0x5D;
    static REG_MAG_OFFSET_Y_MSB        = 0x5E;
    static REG_MAG_OFFSET_Z_LSB        = 0x5F;
    static REG_MAG_OFFSET_Z_MSB        = 0x60;

    // Gyroscope Offset registers
    static REG_GYRO_OFFSET_X_LSB       = 0x61;
    static REG_GYRO_OFFSET_X_MSB       = 0x62;
    static REG_GYRO_OFFSET_Y_LSB       = 0x63;
    static REG_GYRO_OFFSET_Y_MSB       = 0x64;
    static REG_GYRO_OFFSET_Z_LSB       = 0x65;
    static REG_GYRO_OFFSET_Z_MSB       = 0x66;

    // Radius registers
    static REG_ACCEL_RADIUS_LSB        = 0x67;
    static REG_ACCEL_RADIUS_MSB        = 0x68;
    static REG_MAG_RADIUS_LSB          = 0x69;
    static REG_MAG_RADIUS_MSB          = 0x6A;

    // Power modes
    static POWER_MODE_NORMAL           = 0x00;
    static POWER_MODE_LOWPOWER         = 0x01;
    static POWER_MODE_SUSPEND          = 0x02;

    // Operation mode settings
    static OPERATION_MODE_CONFIG       = 0x00;
    static OPERATION_MODE_ACCONLY      = 0x01;
    static OPERATION_MODE_MAGONLY      = 0x02;
    static OPERATION_MODE_GYRONLY      = 0x03;
    static OPERATION_MODE_ACCMAG       = 0x04;
    static OPERATION_MODE_ACCGYRO      = 0x05;
    static OPERATION_MODE_MAGGYRO      = 0x06;
    static OPERATION_MODE_AMG          = 0x07;
    static OPERATION_MODE_IMUPLUS      = 0x08;
    static OPERATION_MODE_COMPASS      = 0x09;
    static OPERATION_MODE_M4G          = 0x0A;
    static OPERATION_MODE_NDOF_FMC_OFF = 0x0B;
    static OPERATION_MODE_NDOF         = 0x0C;

    constructor(bus = 'RPI_1', address = BNO055.ADDRESS_A, mode = BNO055.OPERATION_MODE_NDOF, units = 0) {
        super(bus, address);
        this._mode = mode;

        // Send a thow-away command and ignore any response or I2C errors
        // just to make sure the BNO055 is in a good state and ready to accept
        // commands (this seems to be necessary after a hard power down).
        this.i2c.writeReg8(BNO055.REG_PAGE_ID, 0);

        // switch to config mode
        this._configMode();
        this.i2c.writeReg8(BNO055.REG_PAGE_ID, 0);

        // check the chip ID
        const bnoId = this.i2c.readReg8u(BNO055.REG_CHIP_ID);
        if (bnoId !== BNO055.ID) {
            throw new Error('BNO055 failed to respond');
        }

        // reset the device using the reset command
        this.i2c.writeReg8(BNO055.REG_SYS_TRIGGER, 0x20);

        // wait 650ms after reset for chip to be ready (recommended in datasheet)
        this.i2c.mwait(650);

        // set to normal power mode
        this.i2c.writeReg8(BNO055.REG_PWR_MODE, BNO055.POWER_MODE_NORMAL);

        // default to internal oscillator
        this.i2c.writeReg8(BNO055.REG_SYS_TRIGGER, 0x00);

        // set the unit selection bits
        this.i2c.writeReg8(BNO055.REG_UNIT_SEL, units);

        // set temperature source to gyroscope, as it seems to be more accurate.
        this.i2c.writeReg8(BNO055.REG_TEMP_SOURCE, 0x01);

        // switch to normal operation mode
        this._operationMode();
    }

    _configMode() {
        this.setMode(BNO055.OPERATION_MODE_CONFIG);
    }

    _operationMode() {
        this.setMode(this._mode);
    }

    setMode(mode) {
        this.i2c.writeReg8(BNO055.REG_OPR_MODE, mode & 0xFF);
        // delay for 30ms according to datasheet
        this.i2c.mwait(30);
    }

    getRevision() {
        // read revision values
        const accel = this.i2c.readReg8u(BNO055.REG_ACCEL_REV_ID);
        const mag = this.i2c.readReg8u(BNO055.REG_MAG_REV_ID);
        const gyro = this.i2c.readReg8u(BNO055.REG_GYRO_REV_ID);
        const bl = this.i2c.readReg8u(BNO055.REG_BL_REV_ID);
        const swLsb = this.i2c.readReg8u(BNO055.REG_SW_REV_ID_LSB);
        const swMsb = this.i2c.readReg8u(BNO055.REG_SW_REV_ID_MSB);
        const sw = ((swMsb << 8) | swLsb) & 0xFFFF;
        return [sw, bl, accel, mag, gyro];
    }

    setExternalCrystal(externalCrystal) {
        this._configMode();
        const regVal = externalCrystal ? 0x80 : 0x00;
        this.i2c.writeReg8(BNO055.REG_SYS_TRIGGER, regVal);
        this._operationMode();
    }

    getSystemStatus(runSelfTest = true) {
        let selfTest = false;
        if (runSelfTest) {
            this._configMode();
            const sysTrigger = this.i2c.readReg8u(BNO055.REG_SYS_TRIGGER);
            this.i2c.writeReg8(BNO055.REG_SYS_TRIGGER, sysTrigger | 0x1);
            this.i2c.wait(1);
            selfTest = this.i2c.readReg8u(BNO055.REG_SELFTEST_RESULT);
            this._operationMode();
        }

        const status = this.i2c.readReg8u(BNO055.REG_SYS_STAT);
        const error = this.i2c.readReg8u(BNO055.REG_SYS_ERR);

        return [status, selfTest, error];
    }

    getCalibrationStatus() {
        const calStatus = this.i2c.readReg8u(BNO055.REG_CALIB_STAT);
        const sys = (calStatus >> 6) & 0x03;
        const gyro = (calStatus >> 4) & 0x03;
        const accel = (calStatus >> 2) & 0x03;
        const mag = calStatus & 0x03;
        return [sys, gyro, accel, mag];
    }

    getCalibration() {
        this._configMode();
        const calData = this.i2c.readRegList(BNO055.REG_ACCEL_OFFSET_X_LSB, 22);
        this._operationMode();
        return calData;
    }

    setCalibration(data) {
        if (typeof data === 'undefined' || data.length !== 22) {
            throw new Error('setCalibration Expects a list of 22 bytes of calibration data');
        }

        this._configMode();
        this.i2c.writeRegList(BNO055.REG_ACCEL_OFFSET_X_LSB, data);
        this._operationMode();
    }

    getAxisRemap() {
        const mapConfig = this.i2c.readReg8u(BNO055.REG_AXIS_MAP_CONFIG);
        const z = (mapConfig >> 4) & 0x03;
        const y = (mapConfig >> 2) & 0x03;
        const x = mapConfig & 0x03;
        const signConfig = this.i2c.readReg8u(BNO055.REG_AXIS_MAP_SIGN);
        const xSign = (signConfig >> 2) & 0x01;
        const ySign = (signConfig >> 1) & 0x01;
        const zSign = signConfig & 0x01;
        return [x, y, z, xSign, ySign, zSign];
    }

    setAxisRemap(x, y, z, xSign = BNO055.AXIS_REMAP_POSITIVE, ySign = BNO055.AXIS_REMAP_POSITIVE, zSign = BNO055.AXIS_REMAP_POSITIVE) {
        this._configMode();
        let mapConfig = 0x00;
        mapConfig |= (z & 0x03) << 4;
        mapConfig |= (y & 0x03) << 2;
        mapConfig |= x & 0x03;
        this.i2c.writeReg8(BNO055.REG_AXIS_MAP_CONFIG, mapConfig);

        let signConfig = 0x00;
        signConfig |= (xSign & 0x01) << 2;
        signConfig |= (ySign & 0x01) << 1;
        signConfig |= zSign & 0x01;
        this.i2c.writeReg8(BNO055.REG_AXIS_MAP_SIGN, signConfig);
        this._operationMode();
    }

    _readVector(reg, count = 3) {
        const data = this.i2c.readRegList(reg, count * 2);
        const result = [];
        for (let i = 0; i < count; i++) {
            result[i] = (((data[(i * 2) + 1] & 0xFF) << 8) | (data[(i * 2)] & 0xFF)) & 0xFFFF;
            if (result[i] & 0x8000) {
                result[i] -= 0x10000;
            }
        }
        return result;
    }

    readEuler() {
        const vect = this._readVector(BNO055.REG_EULER_H_LSB);
        return [vect[0] / 16.0, vect[1] / 16.0, vect[2] / 16.0];
    }

    readMagnetometer() {
        const vect = this._readVector(BNO055.REG_MAG_DATA_X_LSB);
        return [vect[0] / 16.0, vect[1] / 16.0, vect[2] / 16.0];
    }

    readGyroscope() {
        const vect = this._readVector(BNO055.REG_GYRO_DATA_X_LSB);
        return [vect[0] / 16.0, vect[1] / 16.0, vect[2] / 16.0];
    }

    readAccelerometer() {
        const vect = this._readVector(BNO055.REG_ACCEL_DATA_X_LSB);
        return [vect[0] / 100.0, vect[1] / 100.0, vect[2] / 100.0];
    }

    readLinearAcceleration() {
        const vect = this._readVector(BNO055.REG_LINEAR_ACCEL_DATA_X_LSB);
        return [vect[0] / 100.0, vect[1] / 100.0, vect[2] / 100.0];
    }

    readGravity() {
        const vect = this._readVector(BNO055.REG_GRAVITY_DATA_X_LSB);
        return [vect[0] / 100.0, vect[1] / 100.0, vect[2] / 100.0];
    }

    readQuaternion() {
        const vect = this._readVector(BNO055.REG_QUATERNION_DATA_W_LSB, 4);
        const scale = (1.0 / (1 << 14));
        return [vect[0] * scale, vect[1] * scale, vect[2] * scale, vect[3] * scale];
    }

    readTemp() {
        return this.i2c.readReg8s(BNO055.REG_TEMP);
    }
}

module.exports = BNO055;
