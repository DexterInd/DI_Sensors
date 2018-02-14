#######################################################################
#
# DistanceSensor
#
# under try/except in case the Distance Sensor is not installed
#######################################################################
try:
    from di_sensors import distance_sensor

except:
    try:
        from mock_package import distance_sensor
        print ("Loading library without distance sensor")
    except:
        pass

# import easy_sensors
from I2C_mutex import Mutex
import time

mutex = Mutex(debug=False)

def _ifMutexAcquire(mutex_enabled=False):
    """
    Acquires the I2C if the ``use_mutex`` parameter of the constructor was set to ``True``.
    """
    if mutex_enabled:
        mutex.acquire()

def _ifMutexRelease(mutex_enabled=False):
    """
    Releases the I2C if the ``use_mutex`` parameter of the constructor was set to ``True``.
    """
    if mutex_enabled:
        mutex.release()


class EasyDistanceSensor(distance_sensor.DistanceSensor):
    """
    Class for the `Distance Sensor`_ device.

    We can create this :py:class:`~easygopigo3.DistanceSensor` object similar to how we create it in the following template.

    .. code-block:: python

        # create an EasyGoPiGo3 object
        gpg3_obj = EasyGoPiGo3()

        # and now let's instantiate a DistanceSensor object through the gpg3_obj object
        distance_sensor = gpg3_obj.init_distance_sensor()

        # read values continuously and print them in the terminal
        while True:
            distance = distance_sensor.read()

            print(distance)

    """
    def __init__(self, port="I2C",gpg=None, use_mutex=False):
        """
        Creates a :py:class:`~easygopigo3.DistanceSensor` object which can be used for interfacing with a `distance sensor`_.

        :param str port = "I2C": Port to which the distance sensor is connected.
        :param easygopigo3.EasyGoPiGo3 gpg = None: Object that's required for instantianting a :py:class:`~easygopigo3.DistanceSensor` object.
        :param bool use_mutex = False: When using multiple threads/processes that access the same resource/device, mutexes should be enabled.
        :raises IOError: If :py:class:`di_sensors.distance_sensor.DistanceSensor` can't be found. Probably the :py:mod:`di_sensors` module isn't installed.
        :raises TypeError: If the ``gpg`` parameter is not a :py:class:`~easygopigo3.EasyGoPiGo3` object.

        To see where the ports are located on the `GoPiGo3`_ robot, please take a look at the following diagram: :ref:`hardware-ports-section`.

        """
        self.descriptor = "Distance Sensor"
        self.use_mutex = use_mutex

        _ifMutexAcquire(self.use_mutex)
        try:
            distance_sensor.DistanceSensor.__init__(self)
        except Exception as e:
            print("Distance Sensor init: {}".format(e))
            raise
        finally:
             _ifMutexRelease(self.use_mutex)

    # Returns the values in cms
    def read_mm(self):
        """
        Reads the distance in millimeters.

        :returns: Distance from target in millimeters.
        :rtype: int

        .. note::

             1. Sensor's range is **5-8,000** millimeters.
             2. When the values are out of the range, it returns **8190**.

        """

        # 8190 is what the sensor sends when it's out of range
        # we're just setting a default value
        mm = 8190
        readings = []
        attempt = 0

        # try 3 times to have a reading that is
        # smaller than 8m or bigger than 5 mm.
        # if sensor insists on that value, then pass it on
        while (mm > 8000 or mm < 5) and attempt < 3:
            _ifMutexAcquire(self.use_mutex)
            try:
                mm = self.read_range_single()
            except Exception as e:
                print(e)
                mm = 0
            finally:
                _ifMutexRelease(self.use_mutex)
            attempt = attempt + 1
            time.sleep(0.001)

        # add the reading to our last 3 readings
        # a 0 value is possible when sensor is not found
        if (mm < 8000 and mm > 5) or mm == 0:
            readings.append(mm)
        if len(readings) > 3:
            readings.pop(0)

        # calculate an average and limit it to 5 > X > 3000
        if len(readings) > 1: # avoid division by 0
            mm = round(sum(readings) / float(len(readings)))
        if mm > 3000:
            mm = 3000

        return mm

    def read(self):
        """
        Reads the distance in centimeters.

        :returns: Distance from target in centimeters.
        :rtype: int

        .. note::

             1. Sensor's range is **0-800** centimeters.
             2. When the values are out of the range, it returns **819**.

        """

        cm = self.read_mm()//10
        return (cm)

    def read_inches(self):
        """
        Reads the distance in inches.

        :returns: Distance from target in inches.
        :rtype: float with one decimal

        .. note::

             1. Sensor's range is **0-314** inches.
             2. Anything that's bigger than **314** inches is returned when the sensor can't detect any target/surface.

        """
        cm = self.read()
        return round(cm / 2.54, 1)

