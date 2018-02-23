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

        ifMutexAcquire(self.use_mutex)
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
            ifMutexRelease(self.use_mutex)

    def reconfig_bus(self):
        self.BNO055.i2c_bus.reconfig_bus()

    def calibrate(self):
        print("calibrating")
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
        print("get calibration status")
        ifMutexAcquire(self.use_mutex)
        try:
            status = self.BNO055.get_calibration_status()[3]
        except Exception as e:
            print("get calibration status FAILED")
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
        # print("safe_read_euler")
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
        :param imu: It's an InertialMeasurementUnit object.
        :return: The heading of the north point measured in degrees. The north point is found at 0 degrees.

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
