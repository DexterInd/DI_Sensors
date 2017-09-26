// https://www.dexterindustries.com/GoPiGo/
// https://github.com/DexterInd/DI_Sensors
//
// Copyright (c) 2017 Dexter Industries
// Released under the MIT license (http://choosealicense.com/licenses/mit/).
// For more information see https://github.com/DexterInd/GoPiGo3/blob/master/LICENSE.md

const BNO055 = require('./BNO055');

class InertialMeasurementUnit {
    constructor(bus = 'RPI_1') {
        this.sensor = new BNO055(bus);
    }

    readEuler() {
        return this.sensor.readEuler();
    }

    readMagnetometer() {
        return this.sensor.readMagnetometer();
    }

    readGyroscope() {
        return this.sensor.readGyroscope();
    }

    readAccelerometer() {
        return this.sensor.readAccelerometer();
    }

    readLinearAcceleration() {
        return this.sensor.readLinearAcceleration();
    }

    readGravity() {
        return this.sensor.readGravity();
    }

    readQuaternion() {
        return this.readQuaternion();
    }

    readTemperature() {
        return this.sensor.readTemp();
    }
}

module.exports = InertialMeasurementUnit;
