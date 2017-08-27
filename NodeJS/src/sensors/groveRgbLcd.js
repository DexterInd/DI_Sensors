// https://www.dexterindustries.com/GoPiGo/
// https://github.com/DexterInd/DI_Sensors
//
// Copyright (c) 2017 Dexter Industries
// Released under the MIT license (http://choosealicense.com/licenses/mit/).
// For more information see https://github.com/DexterInd/GoPiGo3/blob/master/LICENSE.md

const Sensor = require('./base/sensor');

class RgbLcd {
    constructor() {
        this.rgbDevice = new Sensor('RPI_1', 0x62);
        this.txtDevice = new Sensor('RPI_1', 0x3e);
    }

    setRGB(r, g, b) {
        this.rgbDevice.i2c.writeReg8(0, 0);
        this.rgbDevice.i2c.writeReg8(1, 0);
        this.rgbDevice.i2c.writeReg8(0x08, 0xaa);
        this.rgbDevice.i2c.writeReg8(4, r);
        this.rgbDevice.i2c.writeReg8(3, g);
        this.rgbDevice.i2c.writeReg8(2, b);
    }

    textCommand(cmd) {
        this.txtDevice.i2c.writeReg8(0x80, cmd);
    }

    setText(text, noRefresh = false) {
        const refreshCmd = !noRefresh ? 0x01 : 0x02;

        this.textCommand(refreshCmd); // clear or no-refresh
        this.txtDevice.i2c.mwait(5);
        this.textCommand(0x08 | 0x04); // display on, no cursor
        this.textCommand(0x28); // 2 lines
        this.txtDevice.mwait(5);
        let count = 0;
        let row = 0;
        for (let i = 0, len = text.length; i < len; i++) {
            const c = text[i];
            if (c === '\n' || count === 16) {
                count = 0;
                row += 1;
                if (row === 2) {
                    break;
                }
                this.textCommand(0xc0);
                if (c === '\n') {
                    break;
                }
            }
            count++;
            this.txtDevice.i2c.writeReg8(0x40, c.charCodeAt());
        }
    }

    setTextNoRefresh(text) {
        this.setText(text, true);
    }
}

module.exports = RgbLcd;
