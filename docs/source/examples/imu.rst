.. _examples-imu-sensor:

####################
Using the IMU Sensor
####################

In order to run this example program, we need to have a `GoPiGo3`_ because bus ``"GPG3_AD1"`` is used in this case and it's specific to the `GoPiGo3`_ platform.
The ``"GPG3_AD1"`` bus translates to port ``"AD1"`` on the GoPiGo3, so the `IMU Sensor`_ has to be connected to port ``"AD1"``.

We could have gone with the default ``"RPI_1SW"`` bus so it can be used on any platform, but since this is an example, we might as-well show how it's being done with a `GoPiGo3`_.

The source file for this example program can be found `here on github <https://github.com/DexterInd/DI_Sensors/blob/master/Python/Examples/IMUSensor.py>`__.

.. literalinclude:: ../../../Python/Examples/IMUSensor.py
   :language: python
   :lines: 14-

The console output of this script should look like:

.. code-block:: bash

  Example program for reading a Dexter Industries IMU Sensor on a GoPiGo3 AD1 port.
  Magnetometer X: 0.0  Y: 0.0  Z: 0.0 Gyroscope X: 54.9  Y: -25.4  Z: 8.8 Accelerometer X: 9.8  Y: 9.5 Z: -3.5 Euler Heading: 0.0  Roll: 0.0  Pitch: 0.0 Temperature: 31.0C
  Magnetometer X: -44.2  Y: 12.2  Z: 15.8 Gyroscope X: -38.6  Y: 12.4  Z: -116.7 Accelerometer X: -1.2  Y: 4.0 Z: -7.4 Euler Heading: 354.7  Roll: 6.3  Pitch: 13.6 Temperature: 31.0C
  Magnetometer X: -44.6  Y: 15.2  Z: 18.6 Gyroscope X: -11.7  Y: 5.0  Z: 18.5 Accelerometer X: 6.5  Y: 7.0 Z: -1.4 Euler Heading: 354.2  Roll: 6.2  Pitch: 12.6 Temperature: 31.0C
  Magnetometer X: -47.9  Y: 14.5  Z: 17.8 Gyroscope X: 17.1  Y: -23.1  Z: 43.0 Accelerometer X: 6.6  Y: 7.1 Z: -2.2 Euler Heading: 350.6  Roll: 8.3  Pitch: 13.2 Temperature: 31.0C
  Magnetometer X: -30.5  Y: 11.0  Z: 13.0 Gyroscope X: -8.6  Y: -2.1  Z: -0.1 Accelerometer X: 6.2  Y: 5.7 Z: -3.5 Euler Heading: 2.7  Roll: 8.8  Pitch: 12.6 Temperature: 31.0C
  Magnetometer X: -33.2  Y: 10.4  Z: 15.2 Gyroscope X: -87.0  Y: -29.6  Z: 141.0 Accelerometer X: 9.1  Y: 4.8 Z: -1.9 Euler Heading: 332.2  Roll: 15.8  Pitch: 2.1 Temperature: 31.0C


.. _imu sensor: https://www.dexterindustries.com/shop/imu-sensor/
.. _gopigo3: https://www.dexterindustries.com/gopigo3/
.. _grovepi: https://www.dexterindustries.com/grovepi/
.. _brickpi3: https://www.dexterindustries.com/brickpi/
