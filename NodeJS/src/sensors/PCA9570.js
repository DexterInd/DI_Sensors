// https://www.dexterindustries.com/GoPiGo/
// https://github.com/DexterInd/DI_Sensors
//
// Copyright (c) 2017 Dexter Industries
// Released under the MIT license (http://choosealicense.com/licenses/mit/).
// For more information see https://github.com/DexterInd/GoPiGo3/blob/master/LICENSE.md

const Sensor = require('./base/sensor');

class PCA9570 extends Sensor {
    static ADDRESS = 0x24;

    constructor(bus = 'RPI_1') {
        super(bus, PCA9570.ADDRESS);
    }

    setPins(value) {
        this.i2c.write8((value & 0x0F));
    }

    getPins() {
        return this.i2c.read8u() & 0x0F;
    }
}

module.exports = PCA9570;
