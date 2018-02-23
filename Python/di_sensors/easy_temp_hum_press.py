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
import I2C_mutex
from time import sleep

'''
MUTEX HANDLING
'''
mutex = I2C_mutex.Mutex(debug = False)
overall_mutex = mutex.overall_mutex()

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
