// https://www.dexterindustries.com/GoPiGo/
// https://github.com/DexterInd/DI_Sensors
//
// Copyright (c) 2017 Dexter Industries
// Released under the MIT license (http://choosealicense.com/licenses/mit/).
// For more information see https://github.com/DexterInd/GoPiGo3/blob/master/LICENSE.md

const I2C = require('i2c-bus');
const sleep = require('sleep');

class DexterI2C {
    BYTES_LENGTH = 4;

    constructor(bus, address, opts) {
        this.device = opts.device || undefined;

        this.busName = bus;
        this.setAddress(address);
        this.bigEndian = opts.bigEndian || true;

        switch (true) {
        default:
            throw new Error('I2C bus not supported');
        case bus === 'RPI_1':
            this.i2cBus = I2C.openSync(1);
            break;
        case bus === 'GPG3_AD1' || bus === 'GPG3_AD2':
            if (typeof this.device === 'undefined') {
                throw new Error('Device not sent');
            }

            this.gpg = this.device;

            if (bus === 'GPG3_AD1') {
                this.port = this.device.GROVE_1;
            } else if (bus === 'GPG3_AD2') {
                this.port = this.device.GROVE_2;
            }

            this.device.setGroveType(this.port, this.device.GROVE_TYPE.I2C);
            sleep.usleep(1);

            break;
        case bus === 'BP3_1' || bus === 'BP3_2' || bus === 'BP3_3' || bus === 'BP3_4':
            // Not Supported yet
            throw new Error('BrickPi not supported yet. Sorry :-(');
        }
    }

    setAddress(address) {
        this.address = address;
    }

    transfer(dataOut, inBytesLen = 0) {
        if (this.busName === 'RPI_1') {
            const dataLen = dataOut.length;
            let buffer;
            if (dataLen > 1 && inBytesLen === 0) {
                buffer = new Buffer(dataOut);
                this.i2cBus.i2cWriteSync(this.address, buffer.length, buffer);
            } else if (dataLen === 1 && inBytesLen >= 1) {
                buffer = new Buffer(inBytesLen);
                return this.i2cBus.readI2cBlockSync(this.address, dataOut[0], inBytesLen, buffer);
            } else if (dataLen === 0 && inBytesLen >= 1) {
                return this.i2cBus.receiveByteSync(this.address);
            } else {
                throw new Error('I2C operation not supported');
            }
        } else if (this.busName === 'GPG3_AD1' || this.busName === 'GPG3_AD2') {
            if (typeof this.device === 'undefined') {
                throw new Error('Device not sent');
            }

            try {
                return this.device.groveI2cTransfer(this.port, this.address, dataOut, inBytesLen);
            } catch (err) {
                console.log(err);
                throw new Error('[Errno 5] I/O error');
            }
        } else if (this.busName === 'BP3_1' || this.busName === 'BP3_2' || this.busName === 'BP3_3' || this.busName === 'BP3_4') {
            // Not Supported yet
            throw new Error('BrickPi not supported yet. Sorry :-(');
        }

        return false;
    }

    write8(val) {
        val = parseInt(val, 0);
        this.transfer([val]);
    }

    writeReg8(reg, val) {
        val = parseInt(val, 0);
        this.transfer([reg, val]);
    }

    writeReg16(reg, val, bigEndian = undefined) {
        val = parseInt(val, 0);
        if (typeof bigEndian === 'undefined') {
            bigEndian = this.bigEndian;
        }

        if (bigEndian) {
            this.transfer(
                [
                    reg,
                    ((val >> 8) & 0xFF),
                    (val & 0xFF)
                ]
            );
        } else {
            this.transfer([
                reg,
                (val & 0xFF),
                ((val >> 8) & 0xFF)
            ]);
        }
    }

    writeReg32(reg, val, bigEndian = undefined) {
        val = parseInt(val, 0);
        if (typeof bigEndian === 'undefined') {
            bigEndian = this.bigEndian;
        }

        if (bigEndian === true) {
            this.transfer(
                [
                    reg,
                    ((val >> 24) & 0xFF),
                    ((val >> 16) & 0xFF),
                    ((val >> 8) & 0xFF),
                    (val & 0xFF)
                ]
            );
        } else {
            this.transfer([
                reg,
                (val & 0xFF),
                ((val >> 8) & 0xFF),
                ((val >> 16) & 0xFF),
                ((val >> 24) & 0xFF)
            ]);
        }
    }

    wait(s) {
        sleep.sleep(s);
    }

    mwait(ms) {
        sleep.msleep(ms);
    }

    uwait(us) {
        sleep.usleep(us);
    }

    writeRegList(reg, list) {
        if (typeof reg !== 'object') {
            reg = [reg];
        }
        this.transfer(reg.concat(list));
    }

    readByte() {
        return this.readBytes(1);
    }

    readBytes(length = this.BYTES_LENGTH) {
        const buffer = new Buffer(length);
        return this.get(length, buffer);
    }

    read8u() {
        return this.transfer([], 1);
    }

    readReg8u(reg) {
        return this.transfer([reg], 1)[0];
    }

    readReg8s(reg) {
        let val = this.read8u(reg);
        if (val & 0x80) {
            val -= 0x100;
        }
        return val;
    }

    readReg16u(reg, bigEndian = undefined) {
        let val = this.transfer([reg], 2);
        if (typeof bigEndian === 'undefined') {
            bigEndian = this.bigEndian;
        }

        if (bigEndian) {
            val = (val[0] << 8) | val[1];
        } else {
            val = (val[1] << 8) | val[0];
        }

        return val;
    }

    readReg16s(reg, bigEndian = undefined) {
        let val = this.readReg16u(reg, bigEndian);
        if (val & 0x8000) {
            val -= 0x10000;
        }
        return val;
    }

    readRegList(reg, len) {
        return this.transfer([reg], len);
    }
}

module.exports = DexterI2C;
