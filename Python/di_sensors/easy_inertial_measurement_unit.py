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


from di_sensors import inertial_measurement_unit
from di_sensors import BNO055
import I2C_mutex
from math import atan2, pi
from time import sleep

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

class EasyIMUSensor(inertial_measurement_unit.InertialMeasurementUnit):
    '''
    Class for interfacing with the `InertialMeasurementUnit Sensor`_.

    This class compared to :py:class:`~di_sensors.inertial_measurement_unit.InertialMeasurementUnit` uses mutexes that allows a given
    object to be accessed simultaneously from multiple threads/processes.
    Apart from this difference, there may
    also be functions that are more user-friendly than the latter.
    '''

    def __init__(self, port="AD1", use_mutex=False):
        """
        Constructor for initializing link with the `InertialMeasurementUnit Sensor`_.

        :param str port = "AD1": The port to which the IMU sensor gets connected to. By default, it's set to bus ``"AD1"``. Check the :ref:`hardware specs <hardware-interface-section>` for more information about the ports.
        :param bool use_mutex = False: When using multiple threads/processes that access the same resource/device, mutexes should be enabled.
        :raises RuntimeError: When the chip ID is incorrect. This happens when we have a device pointing to the same address, but it's not a `InertialMeasurementUnit Sensor`_.
        :raises ~exceptions.OSError: When the `InertialMeasurementUnit Sensor`_ is not reachable.

        """
        self.use_mutex = use_mutex

        try:
            bus = ports[port]
        except KeyError:
            bus = "RPI_1"

        ifMutexAcquire(self.use_mutex)
        try:
            # print("INSTANTIATING ON PORT {} OR BUS {} WITH MUTEX {}".format(port, bus, use_mutex))
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
            ifMutexRelease(self.use_mutex)

    def reconfig_bus(self):
        """
        If the port configuration got reset, call this method to reconfigure it.

        The idea is that in case the `InertialMeasurementUnit Sensor`_ gets pulled out of the plug or if there's an error on then
        communication line or something else unexpected that puts this sensor to a halt, this method reconfigures
        the connection to the sensor.
        """

        ifMutexAcquire(self.use_mutex)
        self.BNO055.i2c_bus.reconfig_bus()
        ifMutexRelease(self.use_mutex)

    def calibrate(self):
        status = -1
        while status < 3:
            ifMutexAcquire(self.use_mutex)
            try:
                new_status = self.BNO055.get_calibration_status()[3]
            except:
                new_status = -1
            finally:
                ifMutexRelease(self.use_mutex)
            if new_status != status:
                print(new_status)
                status = new_status

    def get_calibration_status(self):
        ifMutexAcquire(self.use_mutex)
        try:
            status = self.BNO055.get_calibration_status()[3]
        except Exception as e:
            print(e)
            status = -1
        finally:
            ifMutexRelease(self.use_mutex)
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
        """
        Read the absolute orientation.

        :returns: Tuple of euler angles in degrees of *heading*, *roll* and *pitch*.
        :rtype: (float,float,float)
        :raises ~exceptions.OSError: When the sensor is not reachable.

        """

        ifMutexAcquire(self.use_mutex)
        try:
            x, y, z = self.read_euler()
        except Exception as e:
            # print("safe read euler: {}".format(str(e)))
            # x, y, z = 0, 0, 0
            raise
        finally:
            ifMutexRelease(self.use_mutex)
        return x,y,z

    def safe_read_magnetometer(self):
        """
        Read the magnetometer values.

        :returns: Tuple containing X, Y, Z values in *micro-Teslas* units. You can check the X, Y, Z axes on the sensor itself.
        :rtype: (float,float,float)

        .. note::

           In case of an exception occurring within this method, a tuple of 3 elements where all values are set to **0** is returned.

        """
        ifMutexAcquire(self.use_mutex)
        try:
            x, y, z = self.read_magnetometer()
        except Exception as e:
            x, y, z = 0, 0, 0
        finally:
            ifMutexRelease(self.use_mutex)
        return x,y,z

    def get_north_point(self):
        """
        Determines the heading of the north point.
        This function doesn't take into account the declination.

        :return: The heading of the north point measured in degrees. The north point is found at **0** degrees.
        :rtype: int

        .. note::

           In case of an exception occurring within this method, **0** is returned.

        """
        ifMutexAcquire(self.use_mutex)
        try:
            x, y, z = self.read_magnetometer()
        except:
            x, y, z = 0,0,0
        finally:
            ifMutexRelease(self.use_mutex)

        # using the x and z axis because the sensor is mounted vertically
        # the sensor's top face is oriented towards the front of the robot

        heading = -atan2(-x, z) * 180 / pi

        # adjust it to 360 degrees range

        if heading < 0:
            heading += 360
        elif heading > 360:
            heading -= 360

        return heading
