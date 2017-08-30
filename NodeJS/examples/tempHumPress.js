const TempHumPress = require('../lib').TempHumPress;

const sensor = new TempHumPress('RPI_1');

console.log('BME280 values',
    'Temp',
    sensor.getTemperatureCelsius(),
    'Press',
    sensor.getPressure(),
    'Hum',
    sensor.getHumidity()
);
