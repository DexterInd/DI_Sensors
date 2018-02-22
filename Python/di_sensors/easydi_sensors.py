from di_sensors import inertial_measurement_unit
from di_sensors import BNO055
from di_sensors import light_color_sensor
from di_sensors import temp_hum_press
from di_sensors import VL53L0X
import I2C_mutex
from math import atan2, pi
from time import sleep
import math


mutex = I2C_mutex.Mutex(debug = False)
overall_mutex = mutex.overall_mutex()

ports = {
    "AD1": "GPG3_AD1",
    "AD2": "GPG3_AD2"
}

def _ifMutexAcquire(mutex_enabled = False):
    """
    Acquires the I2C if the ``use_mutex`` parameter of the constructor was set to ``True``.
    Always acquires if system-wide mutex has been set.
    
    """
    if mutex_enabled or overall_mutex==True:
        mutex.acquire()

def _ifMutexRelease(mutex_enabled = False):
    """
    Releases the I2C if the ``use_mutex`` parameter of the constructor was set to ``True``.

    """
    if mutex_enabled or overall_mutex==True:
        mutex.release()


class EasyIMUSensor(inertial_measurement_unit.InertialMeasurementUnit):
    '''
    Thread-safe IMU
    Orient the IMU for use with a sensor mount
    IMU must be at the back of the GoPiGo, facing backwards
    Supports headings as strings
    '''

    def __init__(self, port="AD1", use_mutex=False):
        self.use_mutex = use_mutex

        try:
            bus = ports[port]
        except KeyError:
            bus = "RPI_1"

        _ifMutexAcquire(self.use_mutex)
        try:
            print("INSTANTIATING ON PORT {} OR BUS {} WITH MUTEX {}".format(port, bus, use_mutex))
            super(self.__class__, self).__init__(bus = bus)
            # on GPG3 we ask that the IMU be at the back of the robot, facing outward
            # We do not support the IMU on GPG2  but leaving the if statement in case
            if bus != "RPI_1":
                self.BNO055.set_axis_remap( BNO055.AXIS_REMAP_X,
                                        BNO055.AXIS_REMAP_Z,
                                        BNO055.AXIS_REMAP_Y,
                                        BNO055.AXIS_REMAP_POSITIVE,
                                        BNO055.AXIS_REMAP_NEGATIVE,
                                        BNO055.AXIS_REMAP_POSITIVE)
        except Exception as e:
            print("Initiating error: "+str(e))
            raise
        finally:
            sleep(0.1)  # add a delay to let the IMU stabilize before control panel can pull from it
            _ifMutexRelease(self.use_mutex)

    def reconfig_bus(self):
        self.BNO055.i2c_bus.reconfig_bus()

    def calibrate(self):
        print("calibrating")
        status = -1
        while status < 3:
            _ifMutexAcquire(self.use_mutex)
            try:
                new_status = self.BNO055.get_calibration_status()[3]
            except:
                new_status = -1
            finally:
                _ifMutexRelease(self.use_mutex)
            if new_status != status:
                print(new_status)
                status = new_status

    def get_calibration_status(self):
        print("get calibration status")
        _ifMutexAcquire(self.use_mutex)
        try:
            status = self.BNO055.get_calibration_status()[3]
        except Exception as e:
            print("get calibration status FAILED")
            print(e)
            status = -1
        finally:
            _ifMutexRelease(self.use_mutex)
        return status

    def get_heading(self, in_heading):
        headings = ["North", "North East",
                    "East", "South East",
                    "South", "South West",
                    "West", "North West",
                    "North"]

        nb_headings = len(headings)-1 # North is listed twice
        heading_index = int(round(in_heading/(360.0/nb_headings),0))
        # sometimes the IMU will return a in_heading of -1000 and higher.
        if heading_index < 0:
            heading_index = 0
        # print("heading {} index {}".format(in_heading, heading_index))
        # print(" {} ".format( headings[heading_index]))
        return(headings[heading_index])

    def safe_read_euler(self):
        # print("safe_read_euler")
        _ifMutexAcquire(self.use_mutex)
        try:
            x, y, z = self.read_euler()
        except Exception as e:
            # print("safe read euler: {}".format(str(e)))
            # x, y, z = 0, 0, 0
            raise
        finally:
            _ifMutexRelease(self.use_mutex)
        return x,y,z

    def safe_read_magnetometer(self):
        _ifMutexAcquire(self.use_mutex)
        try:
            x, y, z = self.read_magnetometer()
        except Exception as e:
            x, y, z = 0, 0, 0
        finally:
            _ifMutexRelease(self.use_mutex)
        return x,y,z

    def get_north_point(self):
        """
        Determines the heading of the north point.
        This function doesn't take into account the declination.
        :param imu: It's an InertialMeasurementUnit object.
        :return: The heading of the north point measured in degrees. The north point is found at 0 degrees.

        """
        _ifMutexAcquire(self.use_mutex)
        try:
            x, y, z = self.read_magnetometer()
        except:
            x, y, z = 0,0,0
        finally:
            _ifMutexRelease(self.use_mutex)

        # using the x and z axis because the sensor is mounted vertically
        # the sensor's top face is oriented towards the front of the robot

        heading = -atan2(-x, z) * 180 / pi

        # adjust it to 360 degrees range

        if heading < 0:
            heading += 360
        elif heading > 360:
            heading -= 360

        return heading



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
        _ifMutexAcquire(self.use_mutex)
        try:
            VL53L0X.VL53L0X(bus = bus)
        except:
            pass
        _ifMutexRelease(self.use_mutex)

        _ifMutexAcquire(self.use_mutex)
        try:
            super(self.__class__, self).__init__(led_state = led_state, bus = bus)
        except Exception as e:
            raise
        finally:
            _ifMutexRelease(self.use_mutex)

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
        _ifMutexAcquire(self.use_mutex)
        try:
            self.set_led(self.led_state)
            r,g,b,c = self.get_raw_colors()
        except:
            pass
        finally:
            _ifMutexRelease(self.use_mutex)
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
            distance_to_hsv = math.sqrt((h - self.known_hsv[color][0])**2 )
            # print((h,s,v), distance_to_hsv)
            if distance_to_hsv < min_distance:
                min_distance = distance_to_hsv
                candidate = color

        return (candidate, self.known_colors[candidate])


class EasyTHPSensor(temp_hum_press.TempHumPress):

    def __init__(self, port="I2C-1", use_mutex=False):
        self.use_mutex = use_mutex

        try:
            bus = ports[port]
        except KeyError:
            bus = "RPI_1"

        _ifMutexAcquire(self.use_mutex)
        try:
            super(self.__class__, self).__init__(bus = bus)
        except Exception as e:
            raise
        finally:
            _ifMutexRelease(self.use_mutex)

    def safe_celsius(self):
        _ifMutexAcquire(self.use_mutex)
        try:
            temp = self.get_temperature_celsius()
        except Exception as e:
            raise
        finally:
            _ifMutexRelease(self.use_mutex)

        return round(temp,0)

    def safe_fahrenheit(self):
        _ifMutexAcquire(self.use_mutex)
        try:
            temp = self.get_temperature_fahrenheit()
        except Exception as e:
            raise
        finally:
            _ifMutexRelease(self.use_mutex)

        return round(temp,0)

    def safe_pressure(self):
        _ifMutexAcquire(self.use_mutex)
        try:
            pressure = self.get_pressure()
        except Exception as e:
            raise
        finally:
            _ifMutexRelease(self.use_mutex)

        return round(pressure,0)

    def safe_humidity(self):
        _ifMutexAcquire(self.use_mutex)
        try:
            humidity = self.get_humidity()
        except Exception as e:
            raise
        finally:
            _ifMutexRelease(self.use_mutex)

        return round(humidity,0)
