// https://www.dexterindustries.com/GoPiGo/
// https://github.com/DexterInd/DI_Sensors
//
// Copyright (c) 2017 Dexter Industries
// Released under the MIT license (http://choosealicense.com/licenses/mit/).
// For more information see https://github.com/DexterInd/GoPiGo3/blob/master/LICENSE.md

const Sensor = require('./sensor');

class DigitalSensor extends Sensor {
    constructor(pin, bus, address, opts) {
        super(bus, address, opts);
        this.pin = pin;
    }

    read() {
        this.i2c.writeRegList(1, [this.pin, 0, 0]);
        this.i2c.mwait(100);
        return this.i2c.readBytes(1)[0];
    }
    write(val) {
        val = parseInt(val, 0);
        this.i2c.writeRegList(2, [this.pin, val, 0]);
    }
}

module.exports = DigitalSensor;
