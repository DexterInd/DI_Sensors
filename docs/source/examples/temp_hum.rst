.. _examples-temphumpress-sensor:

########################################
Temperature Humidity and Pressure Sensor
########################################

In order to run this example program, connect the `Temperature Humidity and Pressure Sensor`_ to an I2C port on whichever platform (`GoPiGo3`_, `GrovePi`_ or `BrickPi3`_)
and then run the following script.

The source file for this example program can be found `here on github <https://github.com/DexterInd/DI_Sensors/blob/master/Python/Examples/TempHumPress.py>`__.

.. literalinclude:: ../../../Python/Examples/TempHumPress.py
   :language: python
   :lines: 14-

The console output of this script should look like:

.. code-block:: bash

  Example program for reading a Dexter Industries Temperature Humidity Pressure Sensor on an I2C port.
  Temperature: 28.139 Humidity: 48.687 Pressure: 101122.691
  Temperature: 28.141 Humidity: 48.698 Pressure: 101122.840
  Temperature: 28.145 Humidity: 48.385 Pressure: 101122.900
  Temperature: 28.151 Humidity: 48.715 Pressure: 101122.889
  Temperature: 28.157 Humidity: 48.436 Pressure: 101122.607
  Temperature: 28.163 Humidity: 48.464 Pressure: 101122.836
  Temperature: 28.171 Humidity: 48.674 Pressure: 101123.085
  Temperature: 28.180 Humidity: 48.120 Pressure: 101123.114

.. _temperature humidity and pressure sensor: https://www.dexterindustries.com/shop/temperature-humidity-pressure-sensor/
.. _gopigo3: https://www.dexterindustries.com/gopigo3/
.. _grovepi: https://www.dexterindustries.com/grovepi/
.. _brickpi3: https://www.dexterindustries.com/brickpi/
