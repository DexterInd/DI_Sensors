// https://www.dexterindustries.com/GoPiGo/
// https://github.com/DexterInd/DI_Sensors
//
// Copyright (c) 2017 Dexter Industries
// Released under the MIT license (http://choosealicense.com/licenses/mit/).
// For more information see https://github.com/DexterInd/GoPiGo3/blob/master/LICENSE.md

const Sensor = require('./sensor');

class AnalogSensor extends Sensor {
    constructor(pin, bus, address, opts) {
        super(bus, address, opts);
        this.pin = pin;
    }

    read(length = this.i2c.BYTES_LENGTH) {
        this.i2c.writeRegList(3, [this.pin, 0, 0]);
        const bytes = this.i2c.readBytes(length);
        return bytes instanceof Buffer ? bytes[1] * 256 + bytes[2] : false;
    }
    write(val) {
        val = parseInt(val, 0);
        this.i2c.writeRegList(4, [this.pin, val, 0]);
    }
}

module.exports = AnalogSensor;
