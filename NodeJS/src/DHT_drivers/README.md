# dht-sensor
node.js module to read the DHT series of humidity and temperature sensors on a Raspberry Pi 2.

### Setup
``` bash
$ npm install dht-sensor --save
```
### Example
``` javascript
var dht = require('dht-sensor');
var current = dht.read(11, 18); // 11 : DHT11, 18 : BCM GPIO  

console.log(current.humidity);
console.log(current.temperature);
```
### Reference
https://github.com/adafruit/Adafruit_Python_DHT
