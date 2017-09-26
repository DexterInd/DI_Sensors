# dht-drivers
node.js module to read the DHT series of humidity and temperature sensors.

### Example
``` javascript
const dht = require('dht-drivers');
const current = dht.read(2, 11, 15); // 2: RaspberryPi (platform ID), 11: DHT11 (module type), 15: (pin)

console.log(current.humidity);
console.log(current.temperature);
```
### Reference
https://github.com/adafruit/Adafruit_Python_DHT
