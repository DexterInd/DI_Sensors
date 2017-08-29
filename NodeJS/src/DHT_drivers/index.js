var dht = require('bindings')('dht-sensor');

// read(platform, sensor, pin | gpio_base, gpio_number?)
// platform: 0 = Beaglebone, 1 = RaspberryPi, 2 = RaspberryPi2
// sensor: 11 = DHT11, 22 = DHT22, 22 = AM2302
// pin | gpio_base: whatever :)
// gpio_number: only for BBB
exports.read = dht.read;
