// https://www.dexterindustries.com/GoPiGo/
// https://github.com/DexterInd/DI_Sensors
//
// Copyright (c) 2017 Dexter Industries
// Released under the MIT license (http://choosealicense.com/licenses/mit/).
// For more information see https://github.com/DexterInd/GoPiGo3/blob/master/LICENSE.md

const Sensor = require('./base/sensor');

class BME280 extends Sensor {
    // BME280 default address.
    ADDRESS = 0x76;

    // Operating Modes
    OSAMPLE_1 = 1;
    OSAMPLE_2 = 2;
    OSAMPLE_4 = 3;
    OSAMPLE_8 = 4;
    OSAMPLE_16 = 5;

    // Standby Settings
    STANDBY_0P5 = 0;
    STANDBY_62P5 = 1;
    STANDBY_125 = 2;
    STANDBY_250 = 3;
    STANDBY_500 = 4;
    STANDBY_1000 = 5;
    STANDBY_10 = 6;
    STANDBY_20 = 7;

    // Filter Settings
    FILTER_OFF = 0;
    FILTER_2 = 1;
    FILTER_4 = 2;
    FILTER_8 = 3;
    FILTER_16 = 4;

    // BME280 Registers
    REG_DIG_T1 = 0x88;  // Trimming parameter registers
    REG_DIG_T2 = 0x8A;
    REG_DIG_T3 = 0x8C;

    REG_DIG_P1 = 0x8E;
    REG_DIG_P2 = 0x90;
    REG_DIG_P3 = 0x92;
    REG_DIG_P4 = 0x94;
    REG_DIG_P5 = 0x96;
    REG_DIG_P6 = 0x98;
    REG_DIG_P7 = 0x9A;
    REG_DIG_P8 = 0x9C;
    REG_DIG_P9 = 0x9E;

    REG_DIG_H1 = 0xA1;
    REG_DIG_H2 = 0xE1;
    REG_DIG_H3 = 0xE3;
    REG_DIG_H4 = 0xE4;
    REG_DIG_H5 = 0xE5;
    REG_DIG_H6 = 0xE6;
    REG_DIG_H7 = 0xE7;

    REG_CHIPID = 0xD0;
    REG_VERSION = 0xD1;
    REG_SOFTRESET = 0xE0;

    REG_STATUS = 0xF3;
    REG_CONTROL_HUM = 0xF2;
    REG_CONTROL = 0xF4;
    REG_CONFIG = 0xF5;
    // REG_DATA = 0xF7
    REG_PRESSURE_DATA = 0xF7;
    REG_TEMP_DATA     = 0xFA;
    REG_HUMIDITY_DATA = 0xFD;

    constructor(bus = 'RPI_1', tMode = BME280.OSAMPLE_1, hMode = BME280.OSAMPLE_1, pMode = BME280.OSAMPLE_1, standby = BME280.STANDBY_250, filter = BME280.FILTER_OFF) {
        super(bus, BME280.ADDRESS, {
            bigEndian: false
        });

        if (
            [
                BME280.OSAMPLE_1,
                BME280.OSAMPLE_2,
                BME280.OSAMPLE_4,
                BME280.OSAMPLE_8,
                BME280.OSAMPLE_16
            ].indexOf(tMode) < 0
        ) {
            throw new Error(`Unexpected tMode ${tMode}. Valid modes are OSAMPLE_1, OSAMPLE_2, OSAMPLE_4, OSAMPLE_8, and OSAMPLE_16.`);
        }
        this._tMode = tMode;

        if (
            [
                BME280.OSAMPLE_1,
                BME280.OSAMPLE_2,
                BME280.OSAMPLE_4,
                BME280.OSAMPLE_8,
                BME280.OSAMPLE_16
            ].indexOf(hMode) < 0
        ) {
            throw new Error(`Unexpected tMode ${hMode}. Valid modes are OSAMPLE_1, OSAMPLE_2, OSAMPLE_4, OSAMPLE_8, and OSAMPLE_16.`);
        }
        this._hMode = hMode;

        if (
            [
                BME280.OSAMPLE_1,
                BME280.OSAMPLE_2,
                BME280.OSAMPLE_4,
                BME280.OSAMPLE_8,
                BME280.OSAMPLE_16
            ].indexOf(pMode) < 0
        ) {
            throw new Error(`Unexpected tMode ${pMode}. Valid modes are OSAMPLE_1, OSAMPLE_2, OSAMPLE_4, OSAMPLE_8, and OSAMPLE_16.`);
        }
        this._pMode = pMode;

        if (
            [
                BME280.STANDBY_0P5,
                BME280.STANDBY_62P5,
                BME280.STANDBY_125,
                BME280.STANDBY_250,
                BME280.STANDBY_500,
                BME280.STANDBY_1000,
                BME280.STANDBY_10,
                BME280.STANDBY_20
            ].indexOf(standby) < 0
        ) {
            throw new Error(`Unexpected tMode ${standby}. Valid values are STANDBY_0P5, STANDBY_10, STANDBY_20, STANDBY_62P5, STANDBY_125, STANDBY_250, STANDBY_500, and STANDBY_1000.`);
        }
        this._standby = standby;

        if (
            [
                BME280.FILTER_OFF,
                BME280.FILTER_2,
                BME280.FILTER_4,
                BME280.FILTER_8,
                BME280.FILTER_16
            ].indexOf(filter) < 0
        ) {
            throw new Error(`Unexpected tMode ${filter}. Valid values are FILTER_OFF, FILTER_2, FILTER_4, FILTER_8, and FILTER_16.`);
        }
        this._filter = filter;

        // Load calibration values
        this._loadCalibration();
        this.i2c.writeReg8(this.REG_CONTROL, 0x24); // Sleep mode
        this.i2c.uwait(2);

        // Set the standby time
        this.i2c.writeReg8(this.REG_CONTROL, ((standby << 5) | (filter << 2)));
        this.i2c.uwait(2);

        // Set the sample modes
        this.i2c.writeReg8(this.REG_CONTROL_HUM, hMode); // Set Humidity Oversample
        this.i2c.writeReg8(this.REG_CONTROL, ((tMode << 5) | (pMode << 2) | 3)); //  Set Temp/Pressure Oversample and enter Normal mode
        this.tFine = 0.0;
    }

    _loadCalibration() {
        // Read calibration data

        this.digT1 = this.i2c.readReg16u(this.REG_DIG_T1);
        this.digT2 = this.i2c.readReg16s(this.REG_DIG_T2);
        this.digT3 = this.i2c.readReg16s(this.REG_DIG_T3);

        this.digP1 = this.i2c.readReg16u(this.REG_DIG_P1);
        this.digP2 = this.i2c.readReg16s(this.REG_DIG_P2);
        this.digP3 = this.i2c.readReg16s(this.REG_DIG_P3);
        this.digP4 = this.i2c.readReg16s(this.REG_DIG_P4);
        this.digP5 = this.i2c.readReg16s(this.REG_DIG_P5);
        this.digP6 = this.i2c.readReg16s(this.REG_DIG_P6);
        this.digP7 = this.i2c.readReg16s(this.REG_DIG_P7);
        this.digP8 = this.i2c.readReg16s(this.REG_DIG_P8);
        this.digP9 = this.i2c.readReg16s(this.REG_DIG_P9);

        this.digH1 = this.i2c.readReg8u(this.REG_DIG_H1);
        this.digH2 = this.i2c.readReg16s(this.REG_DIG_H2);
        this.digH3 = this.i2c.readReg8u(this.REG_DIG_H3);
        this.digH6 = this.i2c.readReg8s(this.REG_DIG_H7);

        let h4 = this.i2c.readReg8s(this.REG_DIG_H4);
        h4 <<= 4;
        this.digH4 = h4 | (this.i2c.readReg8u(this.REG_DIG_H5) & 0x0F);

        let h5 = this.i2c.readReg_8s(this.REG_DIG_H6);
        h5 <<= 4;
        this.digH5 = h5 | (
            this.i2c.readReg8u(this.REG_DIG_H5) >> 4 & 0x0F
        );
    }

    _readRawTemp() {
        // read raw temperature data once it's available
        while (this.i2c.readReg8u(this.REG_STATUS) & 0x08) {
            this.i2c.uwait(2);
        }
        const data = this.i2c.readRegList(this.REG_TEMP_DATA, 3);
        return ((data[0] << 16) | (data[1] << 8) | data[2]) >> 4;
    }

    _readRawPressure() {
        // read raw pressure data once it's available
        while (this.i2c.readReg8u(this.REG_STATUS) & 0x08) {
            this.i2c.uwait(2);
        }
        const data = this.i2c.readRegList(this.REG_PRESSURE_DATA, 3);
        return ((data[0] << 16) | (data[1] << 8) | data[2]) >> 4;
    }

    _readRawHumidity() {
        // read raw humidity data once it's available
        while (this.i2c.readReg8u(this.REG_STATUS) & 0x08) {
            this.i2c.uwait(2);
        }
        const data = this.i2c.readRegList(this.REG_HUMIDITY_DATA, 2);
        return (data[0] << 8) | data[1];
    }

    readTemperature() {
        const rawTemp = parseFloat(this._readRawTemp());
        const temp1 = (rawTemp / 16384.0 - parseFloat(this.digT1) / 1024.0) * parseFloat(this.digT2);
        const temp2 = ((rawTemp / 131072.0 - parseFloat(this.digT1) / 8192.0)
                      * (rawTemp / 131072.0 - parseFloat(this.digT1) / 8192.0)) * parseFloat(this.digT3);
        const temp = temp1 + temp2;
        this.tFine = parseInt(temp, 0);
        return temp1 + temp2 / 5120.0;
    }

    readTemperatureF() {
        return this.readTemperature() * 1.8 + 32;
    }

    readHumidity() {
        const rawHum = parseFloat(this._readRawHumidity());
        let hum = parseFloat(this.tFine) - 76800.0;
        hum = (rawHum - (parseFloat(this.digH4) * 64.0 + parseFloat(this.digH5) / 16384.0 * hum)) * (
            parseFloat(this.digH2) / 65536.0 * (1.0 + parseFloat(this.digH6) / 67108864.0 * hum * (
            1.0 + parseFloat(this.digH3) / 67108864.0 * hum)));
        hum *= (1.0 - parseFloat(this.digH1) * hum / 524288.0);
        hum = hum > 100 ? 100 : hum;
        hum = hum < 0 ? 0 : hum;
        return hum;
    }

    readPressure() {
        const rawPress = parseFloat(this._readRawPressure());

        let press1 = parseFloat(this.tFine) / 2.0 - 64000.0;

        let press2 = press1 * press1 * parseFloat(this.digP6) / 32768.0;
        press2 += press1 * parseFloat(this.digP5) * 2.0;
        press2 = press2 / 4.0 + parseFloat(this.digP4) * 65536.0;
        press1 = (parseFloat(this.digP3) * press1 * press1 / 524288.0 + parseFloat(this.digP2) * press1) / 524288.0;
        press1 = (1.0 + press1 / 32768.0) * parseFloat(this.digP1);
        if (press1 === 0) {
            return 0;
        }

        let press = 1048576.0 - rawPress;
        press = ((press - press2 / 4096.0) * 6250.0) / press1;
        press1 = parseFloat(this.digP9) * press * press / 2147483648.0;
        press2 = press * parseFloat(this.digP8) / 32768.0;

        return press + (press1 + press2 + parseFloat(this.digP7)) / 16.0;
    }

    readPressureInches() {
        // Wrapper to get pressure in inches of Hg
        return this.readPressure() * 0.0002953;
    }

    readDewPoint() {
        return this.readTemperature() - ((100 - this.readHumidity()) / 5);
    }

    readDewPointF() {
        return this.readDewpoint() * 1.8 + 32;
    }
}

module.exports = BME280;
