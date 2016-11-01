import logging
import sys
import time
import BNO055

bno = BNO055.BNO055()

if not bno.begin(mode=BNO055.OPERATION_MODE_NDOF_FMC_OFF):
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

status, self_test, error = bno.get_system_status()
print('System status: {0}'.format(status))
print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
# Print out an error if system status is in error mode.
if status == 0x01:
    print('System error: {0}'.format(error))
    print('See datasheet section 4.3.59 for the meaning.')

# Print BNO055 software revision and other diagnostic data.
sw, bl, accel, mag, gyro = bno.get_revision()
print('Software version:   {0}'.format(sw))
print('Bootloader version: {0}'.format(bl))
print('Accelerometer ID:   0x{0:02X}'.format(accel))
print('Magnetometer ID:    0x{0:02X}'.format(mag))
print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))

print('Reading BNO055 data, press Ctrl-C to quit...')
while True:
    heading, roll, pitch = bno.read_euler()
    # Read the calibration status, 0=uncalibrated and 3=fully calibrated.
    # sys, gyro, accel, mag = bno.get_calibration_status()
    # Print everything out.
    # print('Heading={0:0.2F} Roll={1:0.2F} Pitch={2:0.2F}\tSys_cal={3} Gyro_cal={4} Accel_cal={5} Mag_cal={6}'.format(
    print('Heading={0:0.2F} Roll={1:0.2F} Pitch={2:0.2F}'.format(
          heading, roll, pitch))
    # Other values you can optionally read:
    # Orientation as a quaternion:
    # x,y,z,w = bno.read_quaternion()
    # print('quaternion')
    # print('x={0}\ty={1}\tz={2}\tw={3}'.format(z,y,z,w))
	
    # Sensor temperature in degrees Celsius:
    # temp_c = bno.read_temp()
    # print('temp')
    # print('temp={0}'.format(temp_c))
    # Magnetometer data (in micro-Teslas):
    # x,y,z = bno.read_magnetometer()
    # print('compass')
    # print('x={0}\ty={1}\tz={2}'.format(z,y,z))
    # Gyroscope data (in degrees per second):
    #x,y,z = bno.read_gyroscope()
    # Accelerometer data (in meters per second squared):
    #x,y,z = bno.read_accelerometer()
    # Linear acceleration data (i.e. acceleration from movement, not gravity--
    # returned in meters per second squared):
    #x,y,z = bno.read_linear_acceleration()
    # Gravity acceleration data (i.e. acceleration just from gravity--returned
    # in meters per second squared):
    # x,y,z = bno.read_gravity()
    # Sleep for a second until the next reading.
	
    #print('\n\n')
    time.sleep(.01)
