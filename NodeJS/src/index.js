// https://www.dexterindustries.com/GoPiGo/
// https://github.com/DexterInd/DI_Sensors
//
// Copyright (c) 2017 Dexter Industries
// Released under the MIT license (http://choosealicense.com/licenses/mit/).
// For more information see https://github.com/DexterInd/GoPiGo3/blob/master/LICENSE.md

const DHT = require('./sensors/DHT');
const RgbLcd = require('./sensors/groveRgbLcd');
const BME280 = require('./sensors/BME280');
const BNO055 = require('./sensors/BNO055');
const DistanceSensor = require('./sensors/distanceSensor');
const InertialMeasurementUnit = require('./sensors/inertialMeasurementUnit');
const LightColorSensor = require('./sensors/lightColorSensor');
const PCA9570 = require('./sensors/PCA9570');
const TCS34725 = require('./sensors/TCS34725');
const TempHumPress = require('./sensors/tempHumPress');
const VL53L0X = require('./sensors/VL53L0X');

const sensors = {
    'DHT': DHT,
    'RgbLcd': RgbLcd,
    'BME280': BME280,
    'BNO055': BNO055,
    'DistanceSensor': DistanceSensor,
    'InertialMeasurementUnit': InertialMeasurementUnit,
    'LightColorSensor': LightColorSensor,
    'PCA9570': PCA9570,
    'TCS34725': TCS34725,
    'TempHumPress': TempHumPress,
    'VL53L0X': VL53L0X
};

module.exports = sensors;
