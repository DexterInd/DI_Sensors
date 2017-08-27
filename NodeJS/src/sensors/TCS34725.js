// https://www.dexterindustries.com/GoPiGo/
// https://github.com/DexterInd/DI_Sensors
//
// Copyright (c) 2017 Dexter Industries
// Released under the MIT license (http://choosealicense.com/licenses/mit/).
// For more information see https://github.com/DexterInd/GoPiGo3/blob/master/LICENSE.md

const Sensor = require('./base/sensor');

class TCS34725 extends Sensor {
    ADDRESS          = 0x29;
    ID               = 0x12; // Register should be equal to 0x44 for the TCS34721 or TCS34725, or 0x4D for the TCS34723 or TCS34727.

    COMMAND_BIT      = 0x80;

    ENABLE           = 0x00;
    ENABLE_AIEN      = 0x10; // RGBC Interrupt Enable
    ENABLE_WEN       = 0x08; // Wait enable - Writing 1 activates the wait timer
    ENABLE_AEN       = 0x02; // RGBC Enable - Writing 1 actives the ADC, 0 disables it
    ENABLE_PON       = 0x01; // Power on - Writing 1 activates the internal oscillator, 0 disables it
    ATIME            = 0x01; // Integration time
    WTIME            = 0x03; // Wait time (if ENABLE_WEN is asserted)
    AILTL            = 0x04; // Clear channel lower interrupt threshold
    AILTH            = 0x05;
    AIHTL            = 0x06; // Clear channel upper interrupt threshold
    AIHTH            = 0x07;
    PERS             = 0x0C; // Persistence register - basic SW filtering mechanism for interrupts
    PERS_NONE        = 0b0000; // Every RGBC cycle generates an interrupt
    PERS_1_CYCLE     = 0b0001; // 1 clean channel value outside threshold range generates an interrupt
    PERS_2_CYCLE     = 0b0010; // 2 clean channel values outside threshold range generates an interrupt
    PERS_3_CYCLE     = 0b0011; // 3 clean channel values outside threshold range generates an interrupt
    PERS_5_CYCLE     = 0b0100; // 5 clean channel values outside threshold range generates an interrupt
    PERS_10_CYCLE    = 0b0101; // 10 clean channel values outside threshold range generates an interrupt
    PERS_15_CYCLE    = 0b0110; // 15 clean channel values outside threshold range generates an interrupt
    PERS_20_CYCLE    = 0b0111; // 20 clean channel values outside threshold range generates an interrupt
    PERS_25_CYCLE    = 0b1000; // 25 clean channel values outside threshold range generates an interrupt
    PERS_30_CYCLE    = 0b1001; // 30 clean channel values outside threshold range generates an interrupt
    PERS_35_CYCLE    = 0b1010; // 35 clean channel values outside threshold range generates an interrupt
    PERS_40_CYCLE    = 0b1011; // 40 clean channel values outside threshold range generates an interrupt
    PERS_45_CYCLE    = 0b1100; // 45 clean channel values outside threshold range generates an interrupt
    PERS_50_CYCLE    = 0b1101; // 50 clean channel values outside threshold range generates an interrupt
    PERS_55_CYCLE    = 0b1110; // 55 clean channel values outside threshold range generates an interrupt
    PERS_60_CYCLE    = 0b1111; // 60 clean channel values outside threshold range generates an interrupt
    CONFIG           = 0x0D;
    CONFIG_WLONG     = 0x02; // Choose between short and long (12x) wait times via WTIME
    CONTROL          = 0x0F; // Set the gain level for the sensor
    ID               = 0x12; // 0x44 = TCS34721/TCS34725, 0x4D = TCS34723/TCS34727
    STATUS           = 0x13;
    STATUS_AINT      = 0x10; // RGBC Clean channel interrupt
    STATUS_AVALID    = 0x01; // Indicates that the RGBC channels have completed an integration cycle

    CDATAL           = 0x14; // Clear channel data
    CDATAH           = 0x15;
    RDATAL           = 0x16; // Red channel data
    RDATAH           = 0x17;
    GDATAL           = 0x18; // Green channel data
    GDATAH           = 0x19;
    BDATAL           = 0x1A; // Blue channel data
    BDATAH           = 0x1B;

    GAIN_1X          = 0x00; //  1x gain
    GAIN_4X          = 0x01; //  4x gain
    GAIN_16X         = 0x02; // 16x gain
    GAIN_60X         = 0x03; // 60x gain

    constructor(integrationTime = 0.0024, gain = TCS34725.GAIN_16X, bus = 'RPI_1') {
        super(bus, TCS34725.ADDRESS, {
            bigEndian: false
        });

        // Make sure we're connected to the right sensor.
        const chipId = this.i2c.readReg8u((this.COMMAND_BIT | this.ID));
        if (chipId !== 0x44) {
            throw new Error('Incorrect chip ID.');
        }

        // Set default integration time and gain.
        this.setIntegrationTime(integrationTime);
        this.setGain(gain);

        // Enable the device (by default, the device is in power down mode on bootup).
        this.enable();
    }

    enable() {
        this.i2c.writeReg8((this.COMMAND_BIT | this.ENABLE), this.ENABLE_PON);
        this.i2c.mwait(1);
        this.i2c.writeReg8((this.COMMAND_BIT | this.ENABLE), (this.ENABLE_PON | this.ENABLE_AEN));
    }

    disable() {
        let reg = this.i2c.readReg8u((this.COMMAND_BIT | this.ENABLE));
        reg &= ~(this.ENABLE_PON | this.ENABLE_AEN);
        this.i2c.writeReg8((this.COMMAND_BIT | this.ENABLE), reg);
    }

    setIntegrationtime(time) {
        let val = parseInt(0x100 - (time / 0.0024), 0);
        if (val > 255) {
            val = 255;
        } else if (val < 0) {
            val = 0;
        }
        this.i2c.writeReg8((this.COMMAND_BIT | this.ATIME), val);
        this.integrationTimeVal = val;
    }

    setGain(gain) {
        this.i2c.writeReg8((this.COMMAND_BIT | this.CONTROL), gain);
    }

    setInterrupt(state) {
        this.i2c.writeReg8((this.COMMAND_BIT | this.PERS), this.PERS_NONE);
        let enable = this.i2c.readReg8u((this.COMMAND_BIT | this.ENABLE));
        if (state) {
            enable |= this.ENABLE_AIEN;
        } else {
            enable &= ~this.ENABLE_AIEN;
        }
        this.i2c.writeReg8((this.COMMAND_BIT | this.ENABLE), enable);
    }

    getRawData(delay = true) {
        if (delay) {
            // Delay for the integration time to allow reading immediately after the previous read.
            this.i2c.mwait(((256 - this.integrationTimeVal) * 24));
        }

        const div = ((256 - this.integrationTimeVal) * 1024);
        let r = this.i2c.readReg16u((this.COMMAND_BIT | this.RDATAL)) / div;
        let g = this.i2c.readReg16u((this.COMMAND_BIT | this.GDATAL)) / div;
        let b = this.i2c.readReg16u((this.COMMAND_BIT | this.BDATAL)) / div;
        let c = this.i2c.readReg16u((this.COMMAND_BIT | this.CDATAL)) / div;
        r = r > 1 ? 1 : r;
        g = g > 1 ? 1 : g;
        b = b > 1 ? 1 : b;
        c = c > 1 ? 1 : c;
        return [r, g, b, c];
    }
}

module.exports = TCS34725;
