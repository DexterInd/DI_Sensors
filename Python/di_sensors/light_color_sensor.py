# https://www.dexterindustries.com
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# Python drivers for the Dexter Industries Light Color Sensor

from __future__ import print_function
from __future__ import division

from di_sensors import TCS34725
import time

PCA9570LED = False # set to True for Light Color Sensor boards v1.1.0 and earlier for the PCA9570 to control the LED
if PCA9570LED:
    from di_sensors import PCA9570


class LightColorSensor(object):
    """Drivers for the Dexter Industries Light Color Sensor"""
    
    def __init__(self, sensor_integration_time = 0.0048, sensor_gain = TCS34725.GAIN_16X, led_state = False, bus = "RPI_1"):
        """Initialize the sensor
        
        Keyword arguments:
        integration_time (default 0.0048 seconds) -- Time in seconds for each sample. 0.0024 second (2.4ms) increments. Clipped to the range of 0.0024 to 0.6144 seconds.
        gain (default GAIN_16X) -- The gain constant. Valid values are GAIN_1X, GAIN_4X, GAIN_16X, and GAIN_60X.
        led_state (default False) -- The LED state
        bus (default "RPI_1") -- The I2C bus"""
        self.TCS34725 = TCS34725.TCS34725(sensor_integration_time, sensor_gain, bus)
        if PCA9570LED:
            self.PCA9570 = PCA9570.PCA9570(bus)
        self.set_led(led_state)
    
    # set the state of the LED
    def set_led(self, value, delay = True):
        """Set the LED state
        
        Keyword arguments:
        value -- The LED state
        delay (default True) -- Delay for twice the time it takes to sample. This ensures that the read immediately following the LED change will be correct.
        """
        if PCA9570LED:
            if value:
                self.PCA9570.set_pins(0x00)
            else:
                self.PCA9570.set_pins(0x01)
        else:
            self.TCS34725.set_interrupt(value)
        
        if delay:
            # Delay for twice the integration time to ensure the LED state change has taken effect and a full sample has been made before the next reading.
            time.sleep((((256 - self.TCS34725.integration_time_val) * 0.0024) * 2))
    
    def get_raw_colors(self, delay = True):
        """Read the Red Green Blue and Clear values from the sensor
        
        Keyword arguments:
        delay (default True) -- Delay for the time it takes to sample. This allows immediately consecutive readings that aren't redundant.
        
        Returns the values as a 4-tuple on a scale of 0-1. Red Green Blue Clear."""
        return self.TCS34725.get_raw_data(delay)
