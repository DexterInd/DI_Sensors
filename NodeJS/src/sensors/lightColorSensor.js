// https://www.dexterindustries.com/GoPiGo/
// https://github.com/DexterInd/DI_Sensors
//
// Copyright (c) 2017 Dexter Industries
// Released under the MIT license (http://choosealicense.com/licenses/mit/).
// For more information see https://github.com/DexterInd/GoPiGo3/blob/master/LICENSE.md

const TCS34725 = require('./TCS34725');
const PCA9570 = require('./PCA9570');

class LightColorSensor {
    constructor(
        sensorIntegrationTime = 0.0048,
        sensorGain = TCS34725.GAIN_16X,
        ledState = false,
        bus = 'RPI_1',
        useLightColorSensorBoard = false
    ) {
        this.lightColorDevice = new TCS34725(sensorIntegrationTime, sensorGain, bus);
        this.useLightColorSensorBoard = useLightColorSensorBoard;

        if (useLightColorSensorBoard) {
            this.colorSensorBoard = new PCA9570(bus);
        }

        this.setLed(ledState);
    }

    setLed(value, delay = true) {
        if (this.useLightColorSensorBoard) {
            if (value) {
                this.colorSensorBoard.setPins(0x00);
            } else {
                this.colorSensorBoard.setPins(0x01);
            }
        } else {
            this.lightColorDevice.setInterrupt(value);
        }

        if (delay) {
            this.lightColorDevice.i2c.mwait(
                (((256 - this.lightColorDevice.integrationTimeVal) * 24) * 2)
            );
        }
    }

    getRawColors(delay = true) {
        return this.lightColorDevice.getRawData(delay);
    }
}

module.exports = LightColorSensor;
