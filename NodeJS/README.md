Node.js DI_Sensors
============
Dexter Industries Sensors

Compatibility
-------------

The following Grove compatible devices are supported in Python:

* Dexter Industries:
  * Distance Sensor
  * Inertial Measurement Unit Sensor
  * Light Color Sensor
  * Temperature Humidity Pressure Sensor
* Grove:
  * RGB LCD

Notes for developers
=======

# Features
* Build with [Babel](https://babeljs.io). (ES6 -> ES5)
* Test with [mocha](https://mochajs.org).
* Cover with [istanbul](https://github.com/gotwarlost/istanbul).
* Check with [eslint](eslint.org).
* Deploy with [Travis](travis-ci.org).

# Commands
- `npm run clean` - Remove `lib/` directory
- `npm test` - Run tests. Tests can be written with ES6 (WOW!)
- `npm test:watch` - You can even re-run tests on file changes!
- `npm run cover` - Yes. You can even cover ES6 code.
- `npm run lint` - We recommend using [airbnb-config](https://github.com/airbnb/javascript/tree/master/packages/eslint-config-airbnb). It's fantastic.
- `npm run test:examples` - We recommend writing examples on pure JS for better understanding module usage.
- `npm run build` - Do some magic with ES6 to create ES5 code.
- `npm run prepublish` - Hook for npm. Do all the checks before publishing you module.

License
-------

Please review the [LICENSE.md] file for license information.

[LICENSE.md]: ./LICENSE.md
