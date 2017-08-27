// https://www.dexterindustries.com/GoPiGo/
// https://github.com/DexterInd/DI_Sensors
//
// Copyright (c) 2017 Dexter Industries
// Released under the MIT license (http://choosealicense.com/licenses/mit/).
// For more information see https://github.com/DexterInd/GoPiGo3/blob/master/LICENSE.md

const DHTDevice = require('dht-sensor');

class DHT {
    static DHT11 = 11;
    static DHT22 = 22;
    static AM2302 = 22;
    static SCALE_C = 'c';
    static SCALE_F = 'f';

    constructor(pin, moduleType = DHT.DHT11, scale = DHT.SCALE_C) {
        this.pin = pin;
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
        const needsConversion = typeof scale === 'undefined' || scale === DHT.SCALE_C;

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
        const data = DHTDevice.read(this.moduleType, this.pin);
        let temp =  +(Number(parseFloat(data.temperature).toFixed(2)));
        const hum = +(Number(parseFloat(data.humidity).toFixed(2)));

        if (this.scale === DHT.SCALE_F) {
            temp = this.convertCtoF(temp);
        }

        const heatIndex = +(Number(parseFloat(this.getHeatIndex(temp, hum, this.scale)).toFixed(2)));
        return [temp, hum, heatIndex];
    }
}

module.exports = DHT;
