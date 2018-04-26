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
from di_sensors.easy_mutex import ifMutexAcquire, ifMutexRelease

'''
PORT TRANSLATION
'''
ports = {
    "AD1": "GPG3_AD1",
    "AD2": "GPG3_AD2"
}

class EasyLightColorSensor(light_color_sensor.LightColorSensor):
    """
    Class for interfacing with the `Light Color Sensor`_.

    This class compared to :py:class:`~di_sensors.light_color_sensor.LightColorSensor` uses mutexes that allows a given
    object to be accessed simultaneously from multiple threads/processes.
    Apart from this difference, there may also be functions that are more user-friendly than the latter.

    """

    #: The 6 colors that :py:meth:`~di_sensors.easy_light_color_sensor.EasyLightColorSensor.guess_color_hsv`
    #: method may return upon reading and interpreting a new set of color values.
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

    def __init__(self, port="I2C", led_state = False, use_mutex=False):
        """
        Constructor for initializing a link to the `Light Color Sensor`_.

        :param str port = "I2C": The port to which the distance sensor is connected to. Can also be connected to ports ``"AD1"`` or ``"AD2"`` of the `GoPiGo3`_. If you're passing an **invalid port**, then the sensor resorts to an ``"I2C"`` connection. Check the :ref:`hardware specs <hardware-interface-section>` for more information about the ports.
        :param bool led_state = False: The LED state. If it's set to ``True``, then the LED will turn on, otherwise the LED will stay off. By default, the LED is turned off.
        :param bool use_mutex = False: When using multiple threads/processes that access the same resource/device, mutexes should be enabled.
        :raises ~exceptions.OSError: When the `Light Color Sensor`_ is not reachable.
        :raises ~exceptions.RuntimeError: When the chip ID is incorrect. This happens when we have a device pointing to the same address, but it's not a `Light Color Sensor`_.

        """

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
        """
        Standard algorithm to switch from one color system (**RGB**) to another (**HSV**).

        :param tuple(float,float,float) in_color: The RGB tuple list that gets translated to HSV system. The values of each element of the tuple is between **0** and **1**.
        :return: The translated HSV tuple list. Returned values are *H(0-360)*, *S(0-100)*, *V(0-100)*.
        :rtype: tuple(int, int, int)

        .. important::

           For finding out the differences between **RGB** *(Red, Green, Blue)* color scheme and **HSV** *(Hue, Saturation, Value)*
           please check out `this link <https://www.kirupa.com/design/little_about_color_hsv_rgb.htm>`__.

        """
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


    def safe_raw_colors(self):
        """
        Returns the color as read by the `Light Color Sensor`_.

        The colors detected vary depending on the lighting conditions of the nearby environment.

        :returns: The RGBA values from the sensor. RGBA = Red, Green, Blue, Alpha (or Clear). Range of each element is between **0** and **1**.
        :rtype: tuple(float,float,float,float)

        """
        ifMutexAcquire(self.use_mutex)
        try:
            self.set_led(self.led_state)
            r,g,b,c = self.get_raw_colors()
        except:
            pass
        finally:
            ifMutexRelease(self.use_mutex)
        return (r,g,b,c)

    def safe_rgb(self):
        """
        Detect the RGB color off of the `Light Color Sensor`_.

        :returns: The RGB color in 8-bit format.
        :rtype: tuple(int,int,int)
        """
        colors = self.safe_raw_colors()
        r,g,b,c = list(map(lambda c: int(c*255/colors[3]), colors))
        return r,g,b

    def guess_color_hsv(self, in_color):
        """
        Determines which color `in_color` parameter is closest to in the :py:attr:`~di_sensors.easy_light_color_sensor.EasyLightColorSensor.known_colors` list.

        This method uses the euclidean algorithm for detecting the nearest center to it out of :py:attr:`~di_sensors.easy_light_color_sensor.EasyLightColorSensor.known_colors` list.
        It does work exactly the same as KNN (K-Nearest-Neighbors) algorithm, where `K = 1`.

        :param tuple(float,float,float,float) in_color: A 4-element tuple list for the *Red*, *Green*, *Blue* and *Alpha* channels. The elements are all valued between **0** and **1**.
        :returns: The detected color in string format and then a 3-element tuple describing the color in RGB format. The values of the RGB tuple are between **0** and **1**.
        :rtype: tuple(str,(float,float,float))

        .. important::

           For finding out the differences between **RGB** *(Red, Green, Blue)* color scheme and **HSV** *(Hue, Saturation, Value)*
           please check out `this link <https://www.kirupa.com/design/little_about_color_hsv_rgb.htm>`__.

        """

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
