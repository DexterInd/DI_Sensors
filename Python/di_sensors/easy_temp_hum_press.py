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


from di_sensors import temp_hum_press
from time import sleep

from di_sensors.easy_mutex import ifMutexAcquire, ifMutexRelease

''' 
PORT TRANSLATION
'''
ports = {
    "AD1": "GPG3_AD1",
    "AD2": "GPG3_AD2"
}

class EasyTHPSensor(temp_hum_press.TempHumPress):

    def __init__(self, port="I2C-1", use_mutex=False):
        self.use_mutex = use_mutex

        try:
            bus = ports[port]
        except KeyError:
            bus = "RPI_1"

        ifMutexAcquire(self.use_mutex)
        try:
            super(self.__class__, self).__init__(bus = bus)
        except Exception as e:
            raise
        finally:
            ifMutexRelease(self.use_mutex)

    def safe_celsius(self):
        ifMutexAcquire(self.use_mutex)
        try:
            temp = self.get_temperature_celsius()
        except Exception as e:
            raise
        finally:
            ifMutexRelease(self.use_mutex)

        return round(temp,0)

    def safe_fahrenheit(self):
        ifMutexAcquire(self.use_mutex)
        try:
            temp = self.get_temperature_fahrenheit()
        except Exception as e:
            raise
        finally:
            ifMutexRelease(self.use_mutex)

        return round(temp,0)

    def safe_pressure(self):
        ifMutexAcquire(self.use_mutex)
        try:
            pressure = self.get_pressure()
        except Exception as e:
            raise
        finally:
            ifMutexRelease(self.use_mutex)

        return round(pressure,0)

    def safe_humidity(self):
        ifMutexAcquire(self.use_mutex)
        try:
            humidity = self.get_humidity()
        except Exception as e:
            raise
        finally:
            ifMutexRelease(self.use_mutex)

        return round(humidity,0)
