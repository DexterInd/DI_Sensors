# https://www.dexterindustries.com
#
# Copyright (c) 2018 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#

# EASIER WRAPPERS FOR:
# IMU SENSOR,
# LIGHT AND COLOR SENSOR
# TEMPERATURE, HUMIDITY and PRESSURE SENSOR

# MUTEX SUPPORT WHEN NEEDED


from di_sensors import light_color_sensor
from di_sensors import VL53L0X
import I2C_mutex
from time import sleep
from math import sqrt

'''
MUTEX HANDLING
'''
from di_sensors.easy_mutex import *

''' 
PORT TRANSLATION
'''
ports = {
    "AD1": "GPG3_AD1",
    "AD2": "GPG3_AD2"
}

class EasyLightColorSensor(light_color_sensor.LightColorSensor):
    known_colors = {
        "red":(255,0,0),
        "green":(0,255,0),
        "blue":(0,0,255),
        "yellow":(255,255,0),
        "cyan":(0,255,255),
        "fuchsia":(255,0,255)
    }

    known_hsv = {
        "red":(0,100,100),
        "green":(120,100,100),
        "blue":(240,100,100),
        "yellow":(60,100,100),
        "cyan":(180,100,100),
        "fuchsia":(300,100,100)
    }

    def __init__(self, port="I2C-1", led_state = False, use_mutex=False):
        self.use_mutex = use_mutex

        try:
            bus = ports[port]
        except KeyError:
            bus = "RPI_1"

        # in case there's a distance sensor that hasn't been instanciated yet
        # attempt to move it to another address
        ifMutexAcquire(self.use_mutex)
        try:
            VL53L0X.VL53L0X(bus = bus)
        except:
            pass
        ifMutexRelease(self.use_mutex)

        ifMutexAcquire(self.use_mutex)
        try:
            super(self.__class__, self).__init__(led_state = led_state, bus = bus)
        except Exception as e:
            raise
        finally:
            ifMutexRelease(self.use_mutex)

        self.led_state = led_state

    def translate_to_hsv(self, in_color):
        '''
        standard algorithm to switch from one system (rgb) to the other(hsv)
        incoming are values that go from 0 to 1
        Returned values are h (0-360), s (0-100), v(0-100)
        '''
        r,g,b = in_color

        min_channel = min((r,g,b))
        max_channel = max((r,g,b))

        v = max_channel
        delta = max_channel - min_channel
        if delta < 0.0001:
            s = 0
            h = 0
        else:
            if max_channel > 0:
                s = delta / max_channel
                if r >= max_channel:
                    h = (g - b) / delta
                elif g >= max_channel:
                    h = 2.0 + (b - r) / delta
                else:
                    h = 4 + (r - g ) / delta

                h = h * 60
                if h < 0:
                    h = h + 360

            else:
                s = 0
                h = 0

        return (h,s*100,v*100)


    def get_safe_raw_colors(self, use_mutex=True):
        ifMutexAcquire(self.use_mutex)
        try:
            self.set_led(self.led_state)
            r,g,b,c = self.get_raw_colors()
        except:
            pass
        finally:
            ifMutexRelease(self.use_mutex)
        return (r,g,b,c)

    def get_rgb(self):
        colors = self.get_safe_raw_colors()
        r,g,b,c = list(map(lambda c: int(c*255/colors[3]), colors))
        return r,g,b

    def guess_color_hsv(self, in_color):
        '''
        tries to match an incoming color to a color name
        in_color is the raw readings from the DI Light and Color sensor
        it is a tuple of 4 elements: r, g, b, and light intensity
        expressed in a 0-1 range
        '''
        r,g,b,c = in_color
        # print("incoming: {} {} {} {}".format(r,g,b,c))

        # handle black
        # luminosity is too low, or all color readings are too low
        if c < 0.04 or (r/c < 0.10 and g/c < 0.10 and b/c < 0.10):
            return ("black",(0,0,0))

        # handle white
        # luminosity is high, or all color readings are high
        if c > 0.95 or (r/c > 0.9 and g/c > 0.9 and b/c > 0.9):
            return ("white",(255,255,255))

        # divide by luminosity(clarity) to minimize variations
        h,s,v = self.translate_to_hsv((r/c, g/c, b/c))

        # another black is possible
        # black has a value of 0 and a saturation of 100
        # values of 15 and 95 chosen randomly. They may need to be tweaked
        if v < 15 and s > 95:
            return ("Black",(0,0,0))

        # so is another white
        # white has a value of 100 and a saturation of 0
        # values of 95 and 10 chosen randomly. They may need to be tweaked
        if v > 95 and s < 10:
            return ("White",(255,255,255))

        min_distance = 255
        for color in self.known_hsv:
            # print ("Testing {}".format(color))
            distance_to_hsv = sqrt((h - self.known_hsv[color][0])**2 )
            # print((h,s,v), distance_to_hsv)
            if distance_to_hsv < min_distance:
                min_distance = distance_to_hsv
                candidate = color

        return (candidate, self.known_colors[candidate])

