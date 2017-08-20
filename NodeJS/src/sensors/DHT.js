// https://www.dexterindustries.com/GoPiGo/
// https://github.com/DexterInd/DI_Sensors
//
// Copyright (c) 2017 Dexter Industries
// Released under the MIT license (http://choosealicense.com/licenses/mit/).
// For more information see https://github.com/DexterInd/GoPiGo3/blob/master/LICENSE.md

const DigitalSensor = require('./base/digitalSensor');

class DHT extends DigitalSensor {
    DHT11 = 0;
    DHT22 = 1;
    DHT21 = 2;
    AM2301 = 3;
    SCALE_C = 'c';
    SCALE_F = 'f';

    REG_CMD = 40;

    constructor(pin, address, bus = 'RPI_1', moduleType = DHT.DHT11, scale = DHT.SCALE_C) {
        super(pin, bus, address);

        this.moduleType = moduleType;
        this.scale = scale;
    }

    convertCtoF(temp) {
        return (temp * 1.8) + 32;
    }

    convertFtoC(temp) {
        return (temp - 32) * 1.8;
    }

    getHeatIndex(temp, hum, scale) {
        // http://www.wpc.ncep.noaa.gov/html/heatindex_equation.shtml
        const needsConversion = typeof scale === 'undefined' || scale === this.SCALE_C;

        temp = needsConversion ? this.convertCtoF(temp) : temp;

        // Steadman's result
        let heatIndex = 0.5 * (temp + 61 + (temp - 68) * 1.2 + hum * 0.094);

        // regression equation of Rothfusz is appropriate
        if (temp >= 80) {
            const heatIndexBase = (-42.379                              +
                                2.04901523  * temp                      +
                                10.14333127               * hum         +
                                -0.22475541 * temp        * hum         +
                                -0.00683783 * temp * temp               +
                                -0.05481717               * hum * hum   +
                                0.00122874  * temp * temp * hum         +
                                0.00085282  * temp        * hum * hum   +
                                -0.00000199 * temp * temp * hum * hum);
            // adjustment
            if (hum < 13 && temp <= 112) {
                heatIndex = heatIndexBase - (13 - hum) / 4 * Math.sqrt((17 - Math.abs(temp - 95)) / 17);
            } else if (hum > 85 && temp <= 87) {
                heatIndex = heatIndexBase + ((hum - 85) / 10) * ((87 - temp) / 5);
            } else {
                heatIndex = heatIndexBase;
            }
        }

        return needsConversion ? this.convertFtoC(heatIndex) : heatIndex;
    }

    read() {
        this.i2c.writeRegList(this.REG_CMD, [this.pin, this.moduleType, 0]);

        this.i2c.mwait(500);
        this.i2c.readByte();
        this.i2c.mwait(200);

        const bytes = this.i2c.readBytes(9);

        if (bytes instanceof Buffer) {
            let hex;
            const tempBytes = bytes.slice(1, 5).reverse();
            const humBytes = bytes.slice(5, 9).reverse();

            hex = `0x${tempBytes.toString('hex')}`;
            let temp = (hex & 0x7fffff | 0x800000) * 1.0 / (2 ** 23) * (2 ** ((hex >> 23 & 0xff) - 127));
            temp = +(Number(parseFloat(temp - 0.5).toFixed(2)));
            if (this.scale === this.SCALE_F) {
                temp = this.convertCtoF(temp);
            }

            hex = `0x${humBytes.toString('hex')}`;
            let hum = (hex & 0x7fffff | 0x800000) * 1.0 / (2 ** 23) * (2 ** ((hex >> 23 & 0xff) - 127));
            hum = +(Number(parseFloat(hum - 2).toFixed(2)));

            const heatIndex = +(Number(parseFloat(this.getHeatIndex(temp, hum, this.scale)).toFixed(2)));
            // From: https://github.com/adafruit/DHT-sensor-library/blob/master/DHT.cpp

            return [temp, hum, heatIndex];
        }

        return false;
    }
}

module.exports = DHT;
