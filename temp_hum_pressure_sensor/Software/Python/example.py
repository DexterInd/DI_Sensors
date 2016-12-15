import temp_press_humidity

try:
    sensor = temp_press_humidity.temp_press_humidity(0x76)
    print ('Temperature  = %s deg C'%(sensor.temp_celcius()))
    print ('Temperature  = %s deg F'%(sensor.temp_fahrenheit()))
    print ('Pressure     = %s Pascals'%(sensor.press()))
    print ('Humidity     = %s %% '%(sensor.humidity()))
except IOError:
    print("Sensor not found - quitting")
    exit(-1)


