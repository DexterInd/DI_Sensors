// https://www.dexterindustries.com/GoPiGo/
// https://github.com/DexterInd/DI_Sensors
//
// Copyright (c) 2017 Dexter Industries
// Released under the MIT license (http://choosealicense.com/licenses/mit/).
// For more information see https://github.com/DexterInd/GoPiGo3/blob/master/LICENSE.md

const BME280 = require('./BME280');

class TempHumPress {
    constructor(bus = 'RPI_1') {
        this.sensor = new BME280(bus, BME280.OSAMPLE_2, BME280.OSAMPLE_4, BME280.OSAMPLE_4, BME280.STANDBY_10, BME280.FILTER_8);
    }

    getTemperatureCelsius() {
        return this.sensor.readTemperature();
    }

    getTemperatureFahrenheit() {
        return this.sensor.readTemperatureF();
    }

    getPressure() {
        return this.sensor.readPressure();
    }

    getHumidity() {
        return this.sensor.readHumidity();
    }
}

module.exports = TempHumPress;
