import BME280

class temp_press_humidity(object):
    sensor_bme280=None

    def __init__(self, addr = 0x76):# Set the address and optionally the PWM frequency, which should be 60Hz, but can be off by at least 5%. One measures at about 59.1$
        try:
            self.sensor_bme280 = BME280.BME280(address=addr)
        except:
            # pass
            raise IOError("Sensor not connected")
        return

    def temp_celcius(self):
        try:
            temp=self.sensor_bme280.read_temperature()
            return '{:0.3f}'.format(temp)
        except:
            raise IOError("Sensor not connected")

    def temp_fahrenheit(self):
        try:
            fahrenheit= (self.sensor_bme280.read_temperature()*(9.0/5.0)+32.0)
            return '{0:0.3f}'.format(fahrenheit)
        except:
            raise IOError("Sensor not connected")

    def press(self):
        try:
            press=self.sensor_bme280.read_pressure()
            return '{0:0.3f}'.format(press)
        except:
            raise IOError("Sensor not connected")


    def humidity(self):
        try:
            humidity=self.sensor_bme280.read_humidity()
            return '{0:0.3f}'.format(humidity)
        except:
            raise IOError("Sensor not connected")


