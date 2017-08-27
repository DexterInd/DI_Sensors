// https://www.dexterindustries.com/GoPiGo/
// https://github.com/DexterInd/DI_Sensors
//
// Copyright (c) 2017 Dexter Industries
// Released under the MIT license (http://choosealicense.com/licenses/mit/).
// For more information see https://github.com/DexterInd/GoPiGo3/blob/master/LICENSE.md

const Sensor = require('./base/sensor');

class TCS34725 extends Sensor {
    static ADDRESS          = 0x29;
    static ID               = 0x12; // Register should be equal to 0x44 for the TCS34721 or TCS34725, or 0x4D for the TCS34723 or TCS34727.

    static COMMAND_BIT      = 0x80;

    static ENABLE           = 0x00;
    static ENABLE_AIEN      = 0x10; // RGBC Interrupt Enable
    static ENABLE_WEN       = 0x08; // Wait enable - Writing 1 activates the wait timer
    static ENABLE_AEN       = 0x02; // RGBC Enable - Writing 1 actives the ADC, 0 disables it
    static ENABLE_PON       = 0x01; // Power on - Writing 1 activates the internal oscillator, 0 disables it
    static ATIME            = 0x01; // Integration time
    static WTIME            = 0x03; // Wait time (if ENABLE_WEN is asserted)
    static AILTL            = 0x04; // Clear channel lower interrupt threshold
    static AILTH            = 0x05;
    static AIHTL            = 0x06; // Clear channel upper interrupt threshold
    static AIHTH            = 0x07;
    static PERS             = 0x0C; // Persistence register - basic SW filtering mechanism for interrupts
    static PERS_NONE        = 0b0000; // Every RGBC cycle generates an interrupt
    static PERS_1_CYCLE     = 0b0001; // 1 clean channel value outside threshold range generates an interrupt
    static PERS_2_CYCLE     = 0b0010; // 2 clean channel values outside threshold range generates an interrupt
    static PERS_3_CYCLE     = 0b0011; // 3 clean channel values outside threshold range generates an interrupt
    static PERS_5_CYCLE     = 0b0100; // 5 clean channel values outside threshold range generates an interrupt
    static PERS_10_CYCLE    = 0b0101; // 10 clean channel values outside threshold range generates an interrupt
    static PERS_15_CYCLE    = 0b0110; // 15 clean channel values outside threshold range generates an interrupt
    static PERS_20_CYCLE    = 0b0111; // 20 clean channel values outside threshold range generates an interrupt
    static PERS_25_CYCLE    = 0b1000; // 25 clean channel values outside threshold range generates an interrupt
    static PERS_30_CYCLE    = 0b1001; // 30 clean channel values outside threshold range generates an interrupt
    static PERS_35_CYCLE    = 0b1010; // 35 clean channel values outside threshold range generates an interrupt
    static PERS_40_CYCLE    = 0b1011; // 40 clean channel values outside threshold range generates an interrupt
    static PERS_45_CYCLE    = 0b1100; // 45 clean channel values outside threshold range generates an interrupt
    static PERS_50_CYCLE    = 0b1101; // 50 clean channel values outside threshold range generates an interrupt
    static PERS_55_CYCLE    = 0b1110; // 55 clean channel values outside threshold range generates an interrupt
    static PERS_60_CYCLE    = 0b1111; // 60 clean channel values outside threshold range generates an interrupt
    static CONFIG           = 0x0D;
    static CONFIG_WLONG     = 0x02; // Choose between short and long (12x) wait times via WTIME
    static CONTROL          = 0x0F; // Set the gain level for the sensor
    static ID               = 0x12; // 0x44 = TCS34721/TCS34725, 0x4D = TCS34723/TCS34727
    static STATUS           = 0x13;
    static STATUS_AINT      = 0x10; // RGBC Clean channel interrupt
    static STATUS_AVALID    = 0x01; // Indicates that the RGBC channels have completed an integration cycle

    static CDATAL           = 0x14; // Clear channel data
    static CDATAH           = 0x15;
    static RDATAL           = 0x16; // Red channel data
    static RDATAH           = 0x17;
    static GDATAL           = 0x18; // Green channel data
    static GDATAH           = 0x19;
    static BDATAL           = 0x1A; // Blue channel data
    static BDATAH           = 0x1B;

    static GAIN_1X          = 0x00; //  1x gain
    static GAIN_4X          = 0x01; //  4x gain
    static GAIN_16X         = 0x02; // 16x gain
    static GAIN_60X         = 0x03; // 60x gain

    constructor(integrationTime = 0.0024, gain = TCS34725.GAIN_16X, bus = 'RPI_1') {
        super(bus, TCS34725.ADDRESS, {
            bigEndian: false
        });

        // Make sure we're connected to the right sensor.
        const chipId = this.i2c.readReg8u((TCS34725.COMMAND_BIT | TCS34725.ID));
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
        this.i2c.writeReg8((TCS34725.COMMAND_BIT | TCS34725.ENABLE), TCS34725.ENABLE_PON);
        this.i2c.mwait(1);
        this.i2c.writeReg8((TCS34725.COMMAND_BIT | TCS34725.ENABLE), (TCS34725.ENABLE_PON | TCS34725.ENABLE_AEN));
    }

    disable() {
        let reg = this.i2c.readReg8u((TCS34725.COMMAND_BIT | TCS34725.ENABLE));
        reg &= ~(TCS34725.ENABLE_PON | TCS34725.ENABLE_AEN);
        this.i2c.writeReg8((TCS34725.COMMAND_BIT | TCS34725.ENABLE), reg);
    }

    setIntegrationtime(time) {
        let val = parseInt(0x100 - (time / 0.0024), 0);
        if (val > 255) {
            val = 255;
        } else if (val < 0) {
            val = 0;
        }
        this.i2c.writeReg8((TCS34725.COMMAND_BIT | TCS34725.ATIME), val);
        this.integrationTimeVal = val;
    }

    setGain(gain) {
        this.i2c.writeReg8((TCS34725.COMMAND_BIT | TCS34725.CONTROL), gain);
    }

    setInterrupt(state) {
        this.i2c.writeReg8((TCS34725.COMMAND_BIT | TCS34725.PERS), TCS34725.PERS_NONE);
        let enable = this.i2c.readReg8u((TCS34725.COMMAND_BIT | TCS34725.ENABLE));
        if (state) {
            enable |= TCS34725.ENABLE_AIEN;
        } else {
            enable &= ~TCS34725.ENABLE_AIEN;
        }
        this.i2c.writeReg8((TCS34725.COMMAND_BIT | TCS34725.ENABLE), enable);
    }

    getRawData(delay = true) {
        if (delay) {
            // Delay for the integration time to allow reading immediately after the previous read.
            this.i2c.mwait(((256 - this.integrationTimeVal) * 24));
        }

        const div = ((256 - this.integrationTimeVal) * 1024);
        let r = this.i2c.readReg16u((TCS34725.COMMAND_BIT | TCS34725.RDATAL)) / div;
        let g = this.i2c.readReg16u((TCS34725.COMMAND_BIT | TCS34725.GDATAL)) / div;
        let b = this.i2c.readReg16u((TCS34725.COMMAND_BIT | TCS34725.BDATAL)) / div;
        let c = this.i2c.readReg16u((TCS34725.COMMAND_BIT | TCS34725.CDATAL)) / div;
        r = r > 1 ? 1 : r;
        g = g > 1 ? 1 : g;
        b = b > 1 ? 1 : b;
        c = c > 1 ? 1 : c;
        return [r, g, b, c];
    }
}

module.exports = TCS34725;
