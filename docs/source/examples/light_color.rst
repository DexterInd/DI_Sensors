.. _examples-lightcolor-sensor:

################################
Using the Light and Color Sensor
################################

In order to run this example program, connect the `Light and Color Sensor`_ to an I2C port on whichever platform (`GoPiGo3`_, `GrovePi`_ or `BrickPi3`_)
and then run the following script.

The source file for this example program can be found `here on github <https://github.com/DexterInd/DI_Sensors/blob/master/Python/Examples/LightColorSensor.py>`__.

.. literalinclude:: ../../../Python/Examples/LightColorSensor.py
   :language: python
   :lines: 14-

Here's how the output of the script should look like:

.. code-block:: bash

  Example program for reading a Dexter Industries Light Color Sensor on an I2C port.
  Red: 0.004 Green: 0.004 Blue: 0.004 Clear: 0.013
  Red: 0.005 Green: 0.004 Blue: 0.004 Clear: 0.013
  Red: 0.005 Green: 0.005 Blue: 0.004 Clear: 0.014
  Red: 0.005 Green: 0.005 Blue: 0.004 Clear: 0.015
  Red: 0.005 Green: 0.005 Blue: 0.004 Clear: 0.014
  Red: 0.005 Green: 0.005 Blue: 0.004 Clear: 0.014
  Red: 0.006 Green: 0.005 Blue: 0.005 Clear: 0.015

.. _light and color sensor: https://www.dexterindustries.com/shop/light-color-sensor/
.. _gopigo3: https://www.dexterindustries.com/gopigo3/
.. _grovepi: https://www.dexterindustries.com/grovepi/
.. _brickpi3: https://www.dexterindustries.com/brickpi/
