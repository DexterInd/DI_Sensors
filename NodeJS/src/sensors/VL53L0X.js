// https://www.dexterindustries.com/GoPiGo/
// https://github.com/DexterInd/DI_Sensors
//
// Copyright (c) 2017 Dexter Industries
// Released under the MIT license (http://choosealicense.com/licenses/mit/).
// For more information see https://github.com/DexterInd/GoPiGo3/blob/master/LICENSE.md

const Sensor = require('./base/sensor');

class VL53L0X extends Sensor {
    SYSRANGE_START                              = 0x00;

    SYSTEM_THRESH_HIGH                          = 0x0C;
    SYSTEM_THRESH_LOW                           = 0x0E;

    SYSTEM_SEQUENCE_CONFIG                      = 0x01;
    SYSTEM_RANGE_CONFIG                         = 0x09;
    SYSTEM_INTERMEASUREMENT_PERIOD              = 0x04;

    SYSTEM_INTERRUPT_CONFIG_GPIO                = 0x0A;

    GPIO_HV_MUX_ACTIVE_HIGH                     = 0x84;

    SYSTEM_INTERRUPT_CLEAR                      = 0x0B;

    RESULT_INTERRUPT_STATUS                     = 0x13;
    RESULT_RANGE_STATUS                         = 0x14;

    RESULT_CORE_AMBIENT_WINDOW_EVENTS_RTN       = 0xBC;
    RESULT_CORE_RANGING_TOTAL_EVENTS_RTN        = 0xC0;
    RESULT_CORE_AMBIENT_WINDOW_EVENTS_REF       = 0xD0;
    RESULT_CORE_RANGING_TOTAL_EVENTS_REF        = 0xD4;
    RESULT_PEAK_SIGNAL_RATE_REF                 = 0xB6;

    ALGO_PART_TO_PART_RANGE_OFFSET_MM           = 0x28;

    I2C_SLAVE_DEVICE_ADDRESS                    = 0x8A;

    MSRC_CONFIG_CONTROL                         = 0x60;

    PRE_RANGE_CONFIG_MIN_SNR                    = 0x27;
    PRE_RANGE_CONFIG_VALID_PHASE_LOW            = 0x56;
    PRE_RANGE_CONFIG_VALID_PHASE_HIGH           = 0x57;
    PRE_RANGE_MIN_COUNT_RATE_RTN_LIMIT          = 0x64;

    FINAL_RANGE_CONFIG_MIN_SNR                  = 0x67;
    FINAL_RANGE_CONFIG_VALID_PHASE_LOW          = 0x47;
    FINAL_RANGE_CONFIG_VALID_PHASE_HIGH         = 0x48;
    FINAL_RANGE_CONFIG_MIN_COUNT_RATE_RTN_LIMIT = 0x44;

    PRE_RANGE_CONFIG_SIGMA_THRESH_HI            = 0x61;
    PRE_RANGE_CONFIG_SIGMA_THRESH_LO            = 0x62;

    PRE_RANGE_CONFIG_VCSEL_PERIOD               = 0x50;
    PRE_RANGE_CONFIG_TIMEOUT_MACROP_HI          = 0x51;
    PRE_RANGE_CONFIG_TIMEOUT_MACROP_LO          = 0x52;

    SYSTEM_HISTOGRAM_BIN                        = 0x81;
    HISTOGRAM_CONFIG_INITIAL_PHASE_SELECT       = 0x33;
    HISTOGRAM_CONFIG_READOUT_CTRL               = 0x55;

    FINAL_RANGE_CONFIG_VCSEL_PERIOD             = 0x70;
    FINAL_RANGE_CONFIG_TIMEOUT_MACROP_HI        = 0x71;
    FINAL_RANGE_CONFIG_TIMEOUT_MACROP_LO        = 0x72;
    CROSSTALK_COMPENSATION_PEAK_RATE_MCPS       = 0x20;

    MSRC_CONFIG_TIMEOUT_MACROP                  = 0x46;

    SOFT_RESET_GO2_SOFT_RESET_N                 = 0xBF;
    IDENTIFICATION_MODEL_ID                     = 0xC0;
    IDENTIFICATION_REVISION_ID                  = 0xC2;

    OSC_CALIBRATE_VAL                           = 0xF8;

    GLOBAL_CONFIG_VCSEL_WIDTH                   = 0x32;
    GLOBAL_CONFIG_SPAD_ENABLES_REF_0            = 0xB0;
    GLOBAL_CONFIG_SPAD_ENABLES_REF_1            = 0xB1;
    GLOBAL_CONFIG_SPAD_ENABLES_REF_2            = 0xB2;
    GLOBAL_CONFIG_SPAD_ENABLES_REF_3            = 0xB3;
    GLOBAL_CONFIG_SPAD_ENABLES_REF_4            = 0xB4;
    GLOBAL_CONFIG_SPAD_ENABLES_REF_5            = 0xB5;

    GLOBAL_CONFIG_REF_EN_START_SELECT           = 0xB6;
    DYNAMIC_SPAD_NUM_REQUESTED_REF_SPAD         = 0x4E;
    DYNAMIC_SPAD_REF_EN_START_OFFSET            = 0x4F;
    POWER_MANAGEMENT_GO1_POWER_FORCE            = 0x80;

    VHV_CONFIG_PAD_SCL_SDA__EXTSUP_HV           = 0x89;

    ALGO_PHASECAL_LIM                           = 0x30;
    ALGO_PHASECAL_CONFIG_TIMEOUT                = 0x30;

    ADDRESS_DEFAULT = 0x29;
    ADDRESS = VL53L0X.ADDRESS_DEFAULT;

    VcselPeriodPreRange = 0;
    VcselPeriodFinalRange = 1;

    ioTimeout = 0;
    didTimeout = false;

    constructor(address = 0x2A, timeout = 0.5, bus = 'RPI_1') {
        super(bus, VL53L0X.ADDRESS);

        try {
            this.reset(address);
        } catch (err) {
            console.log(err);
            this.reset(this.ADDRESS);
        }

        this.setAddress(address);
        this.init();
        this.setTimeout(timeout);
    }

    reset(address) {
        try {
            this.i2c.setAddress(address);
            this.i2c.writeReg8(this.SOFT_RESET_GO2_SOFT_RESET_N, 0x00);
        } catch (err) {
            console.log(err);
            // do nothing
        }

        this.ADDRESS = this.ADDRESS_DEFAULT;
        this.i2c.setAddress(this.ADDRESS);

        let value = true;
        let t1 = new Date().getTime();
        while (value) {
            value = this.i2c.readReg8u(this.IDENTIFICATION_MODEL_ID);
            const t2 = new Date().getTime();
            if (t2 - t1 >= 0.1) {
                throw new Error('I/O Error');
            }
            this.i2c.uwait(1);
        }

        this.i2c.writeReg8(this.SOFT_RESET_GO2_SOFT_RESET_N, 0x01);

        value = false;
        t1 = new Date().getTime();
        while (!value) {
            value = this.i2c.readReg8u(this.IDENTIFICATION_MODEL_ID);
            const t2 = new Date().getTime();
            if (t2 - t1 >= 0.1) {
                throw new Error('I/O Error');
            }
            this.i2c.uwait(1);
        }
    }

    setAddress(address) {
        address &= 0x7f;
        try {
            this.i2c.writeReg8(this.I2C_SLAVE_DEVICE_ADDRESS, address);
            this.ADDRESS = address;
            this.i2c.setAddress(this.ADDRESS);
        } catch (err) {
            console.log(err);
            this.i2c.setAddress(address);
            this.i2c.writeReg8(this.I2C_SLAVE_DEVICE_ADDRESS, address);
            this.ADDRESS = address;
            this.i2c.setAddress(this.ADDRESS);
        }
    }

    init() {
        this.i2c.writeReg8(this.VHV_CONFIG_PAD_SCL_SDA__EXTSUP_HV, (this.i2c.readReg8u(this.VHV_CONFIG_PAD_SCL_SDA__EXTSUP_HV) | 0x01)); //  set bit 0

        //  "Set I2C standard mode"
        this.i2c.writeReg8(0x88, 0x00);

        this.i2c.writeReg8(0x80, 0x01);
        this.i2c.writeReg8(0xFF, 0x01);
        this.i2c.writeReg8(0x00, 0x00);
        this.stopVariable = this.i2c.readReg8u(0x91);
        this.i2c.writeReg8(0x00, 0x01);
        this.i2c.writeReg8(0xFF, 0x00);
        this.i2c.writeReg8(0x80, 0x00);

        //  disable SIGNAL_RATE_MSRC (bit 1) and SIGNAL_RATE_PRE_RANGE (bit 4) limit checks
        this.i2c.writeReg8(this.MSRC_CONFIG_CONTROL, (this.i2c.readReg8u(this.MSRC_CONFIG_CONTROL) | 0x12));

        //  set final range signal rate limit to 0.25 MCPS (million counts per second)
        this.setSignalRateLimit(0.25);

        this.i2c.writeReg8(this.SYSTEM_SEQUENCE_CONFIG, 0xFF);

        //  VL53L0X_DataInit() end

        //  VL53L0X_StaticInit() begin

        // spad_count, spad_type_is_aperture, success = this.getSpadInfo()
        const spadInfo = this.getSpadInfo();
        if (!spadInfo[2]) {
            return false;
        }

        //  The SPAD map (RefGoodSpadMap) is read by VL53L0X_get_info_from_device() in
        //  the API, but the same data seems to be more easily readable from
        //  GLOBAL_CONFIG_SPAD_ENABLES_REF_0 through _6, so read it from there
        const refSpadMap = this.i2c.readRegList(this.GLOBAL_CONFIG_SPAD_ENABLES_REF_0, 6);

        //  -- VL53L0X_set_reference_spads() begin (assume NVM values are valid)

        this.i2c.writeReg8(0xFF, 0x01);
        this.i2c.writeReg8(this.DYNAMIC_SPAD_REF_EN_START_OFFSET, 0x00);
        this.i2c.writeReg8(this.DYNAMIC_SPAD_NUM_REQUESTED_REF_SPAD, 0x2C);
        this.i2c.writeReg8(0xFF, 0x00);
        this.i2c.writeReg8(this.GLOBAL_CONFIG_REF_EN_START_SELECT, 0xB4);

        let firstSpadToEnable;
        if (spadInfo[1]) {
            firstSpadToEnable = 12; //  12 is the first aperture spad
        } else {
            firstSpadToEnable = 0;
        }

        let spadsEnabled = 0;

        for (let i = 0, len = 48; i < len; i++) {
            if (i < firstSpadToEnable || spadsEnabled === spadInfo[0]) {
                refSpadMap[parseInt(i / 8, 0)] &= ~(1 << (i % 8));
            } else if (refSpadMap[parseInt(i / 8, 0)] >> (i % 8) & 0x1) {
                spadsEnabled += 1;
            }
        }

        this.i2c.writeRegList(this.GLOBAL_CONFIG_SPAD_ENABLES_REF_0, refSpadMap);

        //  -- VL53L0X_set_reference_spads() end

        //  -- VL53L0X_load_tuning_settings() begin
        //  DefaultTuningSettings from vl53l0x_tuning.h

        this.i2c.writeReg8(0xFF, 0x01);
        this.i2c.writeReg8(0x00, 0x00);

        this.i2c.writeReg8(0xFF, 0x00);
        this.i2c.writeReg8(0x09, 0x00);
        this.i2c.writeReg8(0x10, 0x00);
        this.i2c.writeReg8(0x11, 0x00);

        this.i2c.writeReg8(0x24, 0x01);
        this.i2c.writeReg8(0x25, 0xFF);
        this.i2c.writeReg8(0x75, 0x00);

        this.i2c.writeReg8(0xFF, 0x01);
        this.i2c.writeReg8(0x4E, 0x2C);
        this.i2c.writeReg8(0x48, 0x00);
        this.i2c.writeReg8(0x30, 0x20);

        this.i2c.writeReg8(0xFF, 0x00);
        this.i2c.writeReg8(0x30, 0x09);
        this.i2c.writeReg8(0x54, 0x00);
        this.i2c.writeReg8(0x31, 0x04);
        this.i2c.writeReg8(0x32, 0x03);
        this.i2c.writeReg8(0x40, 0x83);
        this.i2c.writeReg8(0x46, 0x25);
        this.i2c.writeReg8(0x60, 0x00);
        this.i2c.writeReg8(0x27, 0x00);
        this.i2c.writeReg8(0x50, 0x06);
        this.i2c.writeReg8(0x51, 0x00);
        this.i2c.writeReg8(0x52, 0x96);
        this.i2c.writeReg8(0x56, 0x08);
        this.i2c.writeReg8(0x57, 0x30);
        this.i2c.writeReg8(0x61, 0x00);
        this.i2c.writeReg8(0x62, 0x00);
        this.i2c.writeReg8(0x64, 0x00);
        this.i2c.writeReg8(0x65, 0x00);
        this.i2c.writeReg8(0x66, 0xA0);

        this.i2c.writeReg8(0xFF, 0x01);
        this.i2c.writeReg8(0x22, 0x32);
        this.i2c.writeReg8(0x47, 0x14);
        this.i2c.writeReg8(0x49, 0xFF);
        this.i2c.writeReg8(0x4A, 0x00);

        this.i2c.writeReg8(0xFF, 0x00);
        this.i2c.writeReg8(0x7A, 0x0A);
        this.i2c.writeReg8(0x7B, 0x00);
        this.i2c.writeReg8(0x78, 0x21);

        this.i2c.writeReg8(0xFF, 0x01);
        this.i2c.writeReg8(0x23, 0x34);
        this.i2c.writeReg8(0x42, 0x00);
        this.i2c.writeReg8(0x44, 0xFF);
        this.i2c.writeReg8(0x45, 0x26);
        this.i2c.writeReg8(0x46, 0x05);
        this.i2c.writeReg8(0x40, 0x40);
        this.i2c.writeReg8(0x0E, 0x06);
        this.i2c.writeReg8(0x20, 0x1A);
        this.i2c.writeReg8(0x43, 0x40);

        this.i2c.writeReg8(0xFF, 0x00);
        this.i2c.writeReg8(0x34, 0x03);
        this.i2c.writeReg8(0x35, 0x44);

        this.i2c.writeReg8(0xFF, 0x01);
        this.i2c.writeReg8(0x31, 0x04);
        this.i2c.writeReg8(0x4B, 0x09);
        this.i2c.writeReg8(0x4C, 0x05);
        this.i2c.writeReg8(0x4D, 0x04);

        this.i2c.writeReg8(0xFF, 0x00);
        this.i2c.writeReg8(0x44, 0x00);
        this.i2c.writeReg8(0x45, 0x20);
        this.i2c.writeReg8(0x47, 0x08);
        this.i2c.writeReg8(0x48, 0x28);
        this.i2c.writeReg8(0x67, 0x00);
        this.i2c.writeReg8(0x70, 0x04);
        this.i2c.writeReg8(0x71, 0x01);
        this.i2c.writeReg8(0x72, 0xFE);
        this.i2c.writeReg8(0x76, 0x00);
        this.i2c.writeReg8(0x77, 0x00);

        this.i2c.writeReg8(0xFF, 0x01);
        this.i2c.writeReg8(0x0D, 0x01);

        this.i2c.writeReg8(0xFF, 0x00);
        this.i2c.writeReg8(0x80, 0x01);
        this.i2c.writeReg8(0x01, 0xF8);

        this.i2c.writeReg8(0xFF, 0x01);
        this.i2c.writeReg8(0x8E, 0x01);
        this.i2c.writeReg8(0x00, 0x01);
        this.i2c.writeReg8(0xFF, 0x00);
        this.i2c.writeReg8(0x80, 0x00);

        //  -- VL53L0X_load_tuning_settings() end

        //  "Set interrupt config to new sample ready"
        //  -- VL53L0X_SetGpioConfig() begin

        this.i2c.writeReg8(this.SYSTEM_INTERRUPT_CONFIG_GPIO, 0x04);
        this.i2c.writeReg8(this.GPIO_HV_MUX_ACTIVE_HIGH, this.i2c.readReg8u(this.GPIO_HV_MUX_ACTIVE_HIGH) & ~0x10); //  active low
        this.i2c.writeReg8(this.SYSTEM_INTERRUPT_CLEAR, 0x01);

        //  -- VL53L0X_SetGpioConfig() end

        this.measurementTimingBudgetUs = this.get_measurementTimingBudget();

        //  "Disable MSRC and TCC by default"
        //  MSRC = Minimum Signal Rate Check
        //  TCC = Target CentreCheck
        //  -- VL53L0X_SetSequenceStepEnable() begin

        this.i2c.writeReg8(this.SYSTEM_SEQUENCE_CONFIG, 0xE8);

        //  -- VL53L0X_SetSequenceStepEnable() end

        //  "Recalculate timing budget"
        this.setMeasurementTimingBudget(this.measurementTimingBudgetUs);

        // VL53L0X_StaticInit() end

        // VL53L0X_PerformRefCalibration() begin (VL53L0X_perform_ref_calibration())

        // -- VL53L0X_perform_vhv_calibration() begin

        this.i2c.writeReg8(this.SYSTEM_SEQUENCE_CONFIG, 0x01);
        if (!this.performSingleRefCalibration(0x40)) {
            return false;
        }

        // -- VL53L0X_perform_vhv_calibration() end

        // -- VL53L0X_perform_phase_calibration() begin

        this.i2c.writeReg8(this.SYSTEM_SEQUENCE_CONFIG, 0x02);
        if (!this.performSingleRefCalibration(0x00)) {
            return false;
        }

        // -- VL53L0X_perform_phase_calibration() end

        // "restore the previous Sequence Config"
        this.i2c.writeReg8(this.SYSTEM_SEQUENCE_CONFIG, 0xE8);

        // VL53L0X_PerformRefCalibration() end

        return true;
    }

    setSignalRateLimit(limitMcps) {
        if (limitMcps < 0 || limitMcps > 511.99) {
            return false;
        }

        // Q9.7 fixed point format (9 integer bits, 7 fractional bits)
        this.i2c.writeReg16(this.FINAL_RANGE_CONFIG_MIN_COUNT_RATE_RTN_LIMIT, parseInt(limitMcps * (1 << 7), 0));
        return true;
    }

    getSpadInfo() {
        this.i2c.writeReg8(0x80, 0x01);
        this.i2c.writeReg8(0xFF, 0x01);
        this.i2c.writeReg8(0x00, 0x00);

        this.i2c.writeReg8(0xFF, 0x06);
        this.i2c.writeReg8(0x83, this.i2c.readReg8u(0x83) | 0x04);
        this.i2c.writeReg8(0xFF, 0x07);
        this.i2c.writeReg8(0x81, 0x01);

        this.i2c.writeReg8(0x80, 0x01);

        this.i2c.writeReg8(0x94, 0x6b);
        this.i2c.writeReg8(0x83, 0x00);
        this.start_timeout();
        while (this.i2c.readReg8u(0x83) === 0x00) {
            if (this.checkTimeoutExpired()) {
                return [0, 0, false];
            }
        }

        this.i2c.writeReg8(0x83, 0x01);
        const tmp = this.i2c.readReg8u(0x92);

        const count = tmp & 0x7f;
        const typeIsAperture = (tmp >> 7) & 0x01;

        this.i2c.writeReg8(0x81, 0x00);
        this.i2c.writeReg8(0xFF, 0x06);
        this.i2c.writeReg8(0x83, this.i2c.readReg8u(0x83  & ~0x04));
        this.i2c.writeReg8(0xFF, 0x01);
        this.i2c.writeReg8(0x00, 0x01);

        this.i2c.writeReg8(0xFF, 0x00);
        this.i2c.writeReg8(0x80, 0x00);

        return [count, typeIsAperture, true];
    }

    checkTimeoutExpired() {
        const t1 = new Date().getTime();
        if (this.ioTimeout > 0 && (t1 - this.timeoutStart) > this.ioTimeout) {
            return true;
        }
        return false;
    }

    startTimeout() {
        this.timeoutStart = new Date().getTime();
    }

    getMeasurementTimingBudget() {
        const StartOverhead      = 1910; // note that this is different than the value in set_
        const EndOverhead        = 960;
        const MsrcOverhead       = 660;
        const TccOverhead        = 590;
        const DssOverhead        = 690;
        const PreRangeOverhead   = 660;
        const FinalRangeOverhead = 550;

        let budgetUs = StartOverhead + EndOverhead;

        const enables = this.getSequenceStepEnables();
        const timeouts = this.getSequenceStepTimeouts(enables.pre_range);

        if (enables.tcc) {
            budgetUs += (timeouts.msrc_dss_tcc_us + TccOverhead);
        }

        if (enables.dss) {
            budgetUs += 2 * (timeouts.msrc_dss_tcc_us + DssOverhead);
        } else if (enables.msrc) {
            budgetUs += (timeouts.msrc_dss_tcc_us + MsrcOverhead);
        }

        if (enables.pre_range) {
            budgetUs += (timeouts.pre_range_us + PreRangeOverhead);
        }

        if (enables.final_range) {
            budgetUs += (timeouts.final_range_us + FinalRangeOverhead);
        }

        this.measurementTimingBudgetUs = budgetUs; // store for internal reuse
        return budgetUs;
    }

    getSequenceStepEnables() {
        const sequenceConfig = this.i2c.readReg8u(this.SYSTEM_SEQUENCE_CONFIG);
        return {
            'tcc': (sequenceConfig >> 4) & 0x1,
            'msrc': (sequenceConfig >> 2) & 0x1,
            'dss': (sequenceConfig >> 3) & 0x1,
            'pre_range': (sequenceConfig >> 6) & 0x1,
            'final_range': (sequenceConfig >> 7) & 0x1
        };
    }

    getSequenceStepTimeout(preRange) {
        const SequenceStepTimeouts = { 'pre_range_vcsel_periodPclks': 0, 'final_range_vcsel_periodPclks': 0, 'msrc_dss_tcc_mclks': 0, 'pre_range_mclks': 0, 'final_range_mclks': 0, 'msrc_dss_tcc_us': 0, 'pre_range_us': 0, 'final_range_us': 0 };
        SequenceStepTimeouts.pre_range_vcsel_periodPclks = this.getVcselPulsePeriod(this.VcselPeriodPreRange);

        SequenceStepTimeouts.msrc_dss_tcc_mclks = this.i2c.readReg8u(this.MSRC_CONFIG_TIMEOUT_MACROP) + 1;
        SequenceStepTimeouts.msrc_dss_tcc_us = this.timeoutMclksToMicroseconds(SequenceStepTimeouts.msrc_dss_tcc_mclks, SequenceStepTimeouts.pre_range_vcsel_periodPclks);

        SequenceStepTimeouts.pre_range_mclks = this.decodeTimeout(this.i2c.readReg16u(this.PRE_RANGE_CONFIG_TIMEOUT_MACROP_HI));
        SequenceStepTimeouts.pre_range_us = this.timeoutMclksToMicroseconds(SequenceStepTimeouts.pre_range_mclks, SequenceStepTimeouts.pre_range_vcsel_periodPclks);

        SequenceStepTimeouts.final_range_vcsel_periodPclks = this.getVcselPulsePeriod(this.VcselPeriodFinalRange);

        SequenceStepTimeouts.final_range_mclks = this.decodeTimeout(this.i2c.readReg16u(this.FINAL_RANGE_CONFIG_TIMEOUT_MACROP_HI));

        if (preRange) {
            SequenceStepTimeouts.final_range_mclks -= SequenceStepTimeouts.preRangeMclks;
        }

        SequenceStepTimeouts.final_range_us = this.timeoutMclksToMicroseconds(SequenceStepTimeouts.final_range_mclks, SequenceStepTimeouts.final_range_vcsel_periodPclks);

        return SequenceStepTimeouts;
    }

    decodeVcselPeriod(regVal) {
        return (((regVal) + 1) << 1);
    }

    getVcselPulsePeriod(type) {
        if (type === this.VcselPeriodPreRange) {
            return this.decodeVcselPeriod(this.i2c.readReg8u(this.PRE_RANGE_CONFIG_VCSEL_PERIOD));
        } else if (type === this.VcselPeriodFinalRange) {
            return this.decodeVcselPeriod(this.i2c.readReg8u(this.FINAL_RANGE_CONFIG_VCSEL_PERIOD));
        }
        return 255;
    }

    timeoutMclksToMicroseconds(timeoutPeriodMclks, vcselPeriodPclks) {
        const macroPeriodNs = this.calcMacroPeriod(vcselPeriodPclks);
        return ((timeoutPeriodMclks * macroPeriodNs) + (macroPeriodNs / 2)) / 1000;
    }

    calcMacroPeriod(vcselPeriodPclks) {
        return (((2304 * vcselPeriodPclks * 1655) + 500) / 1000);
    }

    decodeTimeout(regVal) {
        return ((regVal & 0x00FF) << ((regVal & 0xFF00) >> 8)) + 1;
    }

    setMeasurementTimingBudget(budgetUs) {
        const StartOverhead      = 1320; // note that this is different than the value in get_
        const EndOverhead        = 960;
        const MsrcOverhead       = 660;
        const TccOverhead        = 590;
        const DssOverhead        = 690;
        const PreRangeOverhead   = 660;
        const FinalRangeOverhead = 550;

        const MinTimingBudget = 20000;

        if (budgetUs < MinTimingBudget) {
            return false;
        }

        let usedBudgetUs = StartOverhead + EndOverhead;

        const enables = this.getSequenceStepEnables();
        const timeouts = this.getSequenceStepTimeout(enables.pre_range);

        if (enables.tcc) {
            usedBudgetUs += (timeouts.msrc_dss_tcc_us + TccOverhead);
        }

        if (enables.dss) {
            usedBudgetUs += 2 * (timeouts.msrc_dss_tcc_us + DssOverhead);
        } else if (enables.msrc) {
            usedBudgetUs += (timeouts.msrc_dss_tcc_us + MsrcOverhead);
        }

        if (enables.pre_range) {
            usedBudgetUs += (timeouts.pre_range_us + PreRangeOverhead);
        }

        if (enables.final_range) {
            usedBudgetUs += FinalRangeOverhead;
        }

        if (usedBudgetUs > budgetUs) {
            return false;
        }

        const finalRangeTimeoutUs = budgetUs - usedBudgetUs;
        let finalRangeTimeoutMclks = this.timeoutMicrosecondsToMclks(finalRangeTimeoutUs, timeouts.final_range_vcsel_periodPclks);

        if (enables.pre_range) {
            finalRangeTimeoutMclks += timeouts.pre_range_mclks;
        }

        this.i2c.writeReg16(this.FINAL_RANGE_CONFIG_TIMEOUT_MACROP_HI, this.encodeTimeout(finalRangeTimeoutMclks));

        this.measurementTimingBudgetUs = budgetUs;

        return true;
    }

    encodeTimeout(timeoutMclks) {
        let lsByte = 0;
        let msByte = 0;

        if (timeoutMclks > 0) {
            lsByte = timeoutMclks - 1;

            while ((parseInt(lsByte, 0) & 0xFFFFFF00) > 0) {
                lsByte /= 2; // >>=
                msByte += 1;
            }

            return ((msByte << 8) | (parseInt(lsByte, 0) & 0xFF));
        }

        return 0;
    }

    timeoutMicrosecondsToMclks(timeoutPeriodUs, vcselPeriodPclks) {
        const macroPeriodNs = this.calcMacroPeriod(vcselPeriodPclks);
        return (((timeoutPeriodUs * 1000) + (macroPeriodNs / 2)) / macroPeriodNs);
    }

    performSingleRefCalibration(vhvInitByte) {
        this.i2c.writeReg8(this.SYSRANGE_START, 0x01 | vhvInitByte);

        this.startTimeout();
        while ((this.i2c.readReg8u(this.RESULT_INTERRUPT_STATUS) & 0x07) === 0) {
            if (this.checkTimeoutExpired()) {
                return false;
            }
        }

        this.i2c.writeReg8(this.SYSTEM_INTERRUPT_CLEAR, 0x01);
        this.i2c.writeReg8(this.SYSRANGE_START, 0x00);

        return true;
    }

    setTimeout(timeout) {
        this.ioTimeout = timeout;
    }

    startContinuous(periodMs = 0) {
        this.i2c.writeReg8(0x80, 0x01);
        this.i2c.writeReg8(0xFF, 0x01);
        this.i2c.writeReg8(0x00, 0x00);
        this.i2c.writeReg8(0x91, this.stopVariable);
        this.i2c.writeReg8(0x00, 0x01);
        this.i2c.writeReg8(0xFF, 0x00);
        this.i2c.writeReg8(0x80, 0x00);

        if (periodMs !== 0) {
            const oscCalibrateVal = this.i2c.readReg16u(this.OSC_CALIBRATE_VAL);

            if (oscCalibrateVal !== 0) {
                periodMs *= oscCalibrateVal;
            }

            this.i2c.writeReg32(this.SYSTEM_INTERMEASUREMENT_PERIOD, periodMs);
            this.i2c.writeReg8(this.SYSRANGE_START, 0x04);
        } else {
            this.i2c.writeReg8(this.SYSRANGE_START, 0x02);
        }
    }

    readRangeContinuousMillimiters() {
        this.startTimeout();

        while ((this.i2c.readReg8u(this.RESULT_INTERRUPT_STATUS) & 0x07) === 0) {
            if (this.checkTimeoutExpired()) {
                this.didTimeout = true;
                console.log('readRangeContinuousMillimiters timeout');
            }
        }

        const range = this.i2c.readReg16u(this.RESULT_RANGE_STATUS + 10);
        this.i2c.writeReg8(this.SYSTEM_INTERRUPT_CLEAR, 0x01);
        return range;
    }

    timeoutOccurred() {
        const ret = this.didTimeout;
        this.didTimeout = false;
        return ret;
    }

    setVcselPulsePeriod(type, periodPclks) {
        const vcselPeriodReg = this.encodeVcselPeriod(periodPclks);

        const enables = this.getSequenceStepEnables();
        const timeouts = this.getSequenceStepTimeouts(enables.pre_range);

        if (type === this.VcselPeriodPreRange) {
            if (periodPclks === 12) {
                this.i2c.writeReg8(this.PRE_RANGE_CONFIG_VALID_PHASE_HIGH, 0x18);
            } else if (periodPclks === 14) {
                this.i2c.writeReg8(this.PRE_RANGE_CONFIG_VALID_PHASE_HIGH, 0x30);
            } else if (periodPclks === 16) {
                this.i2c.writeReg8(this.PRE_RANGE_CONFIG_VALID_PHASE_HIGH, 0x40);
            } else if (periodPclks === 18) {
                this.i2c.writeReg8(this.PRE_RANGE_CONFIG_VALID_PHASE_HIGH, 0x50);
            } else {
                return false;
            }

            this.i2c.writeReg8(this.PRE_RANGE_CONFIG_VALID_PHASE_LOW, 0x08);

            this.i2c.writeReg8(this.PRE_RANGE_CONFIG_VCSEL_PERIOD, vcselPeriodReg);

            const newPreRangeTimeoutMclks = this.timeoutMicrosecondsToMclks(timeouts.pre_range_us, periodPclks);

            this.i2c.writeReg16(this.PRE_RANGE_CONFIG_TIMEOUT_MACROP_HI, this.encodeTimeout(newPreRangeTimeoutMclks));

            const newMsrcTimeoutMclks = this.timeoutMicrosecondsToMclks(timeouts.msrc_dss_tcc_us, periodPclks);

            if (newMsrcTimeoutMclks > 256) {
                this.i2c.writeReg8(this.MSRC_CONFIG_TIMEOUT_MACROP, 255);
            } else {
                this.i2c.writeReg8(this.MSRC_CONFIG_TIMEOUT_MACROP, (newMsrcTimeoutMclks - 1));
            }
        } else if (type === this.VcselPeriodFinalRange) {
            if (periodPclks === 8) {
                this.i2c.writeReg8(this.FINAL_RANGE_CONFIG_VALID_PHASE_HIGH, 0x10);
                this.i2c.writeReg8(this.FINAL_RANGE_CONFIG_VALID_PHASE_LOW,  0x08);
                this.i2c.writeReg8(this.GLOBAL_CONFIG_VCSEL_WIDTH, 0x02);
                this.i2c.writeReg8(this.ALGO_PHASECAL_CONFIG_TIMEOUT, 0x0C);
                this.i2c.writeReg8(0xFF, 0x01);
                this.i2c.writeReg8(this.ALGO_PHASECAL_LIM, 0x30);
                this.i2c.writeReg8(0xFF, 0x00);
            } else if (periodPclks === 10) {
                this.i2c.writeReg8(this.FINAL_RANGE_CONFIG_VALID_PHASE_HIGH, 0x28);
                this.i2c.writeReg8(this.FINAL_RANGE_CONFIG_VALID_PHASE_LOW,  0x08);
                this.i2c.writeReg8(this.GLOBAL_CONFIG_VCSEL_WIDTH, 0x03);
                this.i2c.writeReg8(this.ALGO_PHASECAL_CONFIG_TIMEOUT, 0x09);
                this.i2c.writeReg8(0xFF, 0x01);
                this.i2c.writeReg8(this.ALGO_PHASECAL_LIM, 0x20);
                this.i2c.writeReg8(0xFF, 0x00);
            } else if (periodPclks === 12) {
                this.i2c.writeReg8(this.FINAL_RANGE_CONFIG_VALID_PHASE_HIGH, 0x38);
                this.i2c.writeReg8(this.FINAL_RANGE_CONFIG_VALID_PHASE_LOW,  0x08);
                this.i2c.writeReg8(this.GLOBAL_CONFIG_VCSEL_WIDTH, 0x03);
                this.i2c.writeReg8(this.ALGO_PHASECAL_CONFIG_TIMEOUT, 0x08);
                this.i2c.writeReg8(0xFF, 0x01);
                this.i2c.writeReg8(this.ALGO_PHASECAL_LIM, 0x20);
                this.i2c.writeReg8(0xFF, 0x00);
            } else if (periodPclks === 14) {
                this.i2c.writeReg8(this.FINAL_RANGE_CONFIG_VALID_PHASE_HIGH, 0x48);
                this.i2c.writeReg8(this.FINAL_RANGE_CONFIG_VALID_PHASE_LOW,  0x08);
                this.i2c.writeReg8(this.GLOBAL_CONFIG_VCSEL_WIDTH, 0x03);
                this.i2c.writeReg8(this.ALGO_PHASECAL_CONFIG_TIMEOUT, 0x07);
                this.i2c.writeReg8(0xFF, 0x01);
                this.i2c.writeReg8(this.ALGO_PHASECAL_LIM, 0x20);
                this.i2c.writeReg8(0xFF, 0x00);
            } else {
                return false;
            }

            this.i2c.writeReg8(this.FINAL_RANGE_CONFIG_VCSEL_PERIOD, vcselPeriodReg);
            let newFinalRangeTimeoutMclks = this.timeoutMicrosecondsToMclks(timeouts.final_range_us, periodPclks);

            if (enables.pre_range) {
                newFinalRangeTimeoutMclks += timeouts.pre_range_mclks;
            }

            this.i2c.writeReg16(this.FINAL_RANGE_CONFIG_TIMEOUT_MACROP_HI, this.encodeTimeout(newFinalRangeTimeoutMclks));
        } else {
            return false;
        }

        this.setMeasurementTimingBudget(this.measurementTimingBudgetUs);

        const sequenceConfig = this.i2c.readReg8u(this.SYSTEM_SEQUENCE_CONFIG);
        this.i2c.writeReg8(this.SYSTEM_SEQUENCE_CONFIG, 0x02);
        this.performSingleRefCalibration(0x0);
        this.i2c.writeReg8(this.SYSTEM_SEQUENCE_CONFIG, sequenceConfig);

        return true;
    }

    readRangeSingleMillimiters() {
        this.i2c.writeReg8(0x80, 0x01);
        this.i2c.writeReg8(0xFF, 0x01);
        this.i2c.writeReg8(0x00, 0x00);
        this.i2c.writeReg8(0x91, this.stopVariable);
        this.i2c.writeReg8(0x00, 0x01);
        this.i2c.writeReg8(0xFF, 0x00);
        this.i2c.writeReg8(0x80, 0x00);

        this.i2c.writeReg8(this.SYSRANGE_START, 0x01);

        this.startTimeout();
        while (this.i2c.readReg8u(this.SYSRANGE_START) & 0x01) {
            if (this.checkTimeoutExpired()) {
                this.didTimeout = true;
                console.log('read_range_single_millimeters timeout');
            }
        }
        return this.readRangeContinuousMillimeters();
    }

    encodeVcselPeriod(periodPclks) {
        return ((periodPclks >> 1) - 1);
    }
}

module.exports = VL53L0X;
