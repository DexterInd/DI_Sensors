// https://www.dexterindustries.com/GoPiGo/
// https://github.com/DexterInd/DI_Sensors
//
// Copyright (c) 2017 Dexter Industries
// Released under the MIT license (http://choosealicense.com/licenses/mit/).
// For more information see https://github.com/DexterInd/GoPiGo3/blob/master/LICENSE.md

const VL53L0X = require('./VL53L0X');

class DistanceSensor {
    constructor(bus = 'RPI_1') {
        this.sensor = new VL53L0X(bus);
        this.sensor.setSignalRateLimit(0.1);
        this.sensor.setVcselPulsePeriod(this.sensor.VcselPeriodPreRange, 18);
        this.sensor.setVcselPulsePeriod(this.sensor.VcselPeriodFinalRange, 14);
    }

    startContinuous(periodMs = 0) {
        this.startContinuous.startContinuous(periodMs);
    }

    readRangeContinuous() {
        return this.sensor.readRangeContinuousMillimiters();
    }

    readRangeSingle() {
        return this.sensor.readRangeSingleMillimiters();
    }

    timeoutOccurred() {
        return this.sensor.timeoutOccurred();
    }
}

module.exports = DistanceSensor;
