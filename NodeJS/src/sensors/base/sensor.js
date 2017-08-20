// https://www.dexterindustries.com/GoPiGo/
// https://github.com/DexterInd/DI_Sensors
//
// Copyright (c) 2017 Dexter Industries
// Released under the MIT license (http://choosealicense.com/licenses/mit/).
// For more information see https://github.com/DexterInd/GoPiGo3/blob/master/LICENSE.md

const _ = require('lodash');

const EventEmitter = require('events');
const DexterI2C = require('../dexterI2c');

class Sensor extends EventEmitter {
    WATCH_DELAY = 100;
    // ms
    STREAM_DELAY = 100;
    // ms

    constructor(bus, address, opts) {
        super();

        this.i2c = new DexterI2C(bus, address, opts);
        this.lastValue = 0;
        this.currentValue = 0;
        this.streamInterval = this.watchInterval = undefined;
        this.watchDelay = this.WATCH_DELAY;
        this.streamDelay = this.STREAM_DELAY;
    }

    read() {}
    write() {}
    stream(delay = this.streamDelay, callBack) {
        const _this = this;

        this.stopStream();
        this.streamInterval = setInterval(() => {
            const res = _this.read();
            callBack(res);
        }, delay);
    }
    stopStream() {
        clearInterval(this.streamInterval);
    }
    watch(delay = this.watchDelay) {
        const _this = this;

        this.stopWatch();
        this.watchInterval = setInterval(() => {
            const res = _this.read();

            _this.lastValue = _this.currentValue;
            this.currentValue = res;

            if (!_.isEqual(_this.currentValue, _this.lastValue)) {
                _this.emit('change', _this.currentValue);
            }
        }, delay);
    }
    stopWatch() {
        clearInterval(this.watchInterval);
    }
}

module.exports = Sensor;
