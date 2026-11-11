.. _examples-lightcolor-sensor:

################################
Using the Light and Color Sensor
################################

In this short section, we get to see how one can read data off of the `Light and Color Sensor`_ without having to fine-tune the sensor or to deal with hard-to-understand concepts.
Before anything else, connect the `Light and Color Sensor`_ to an I2C port on whichever platform (be it a `GoPiGo3`_, `GrovePi`_ or a `BrickPi3`_) and then run the following script.

The source file for this example program can be found `here on github <https://github.com/DexterInd/DI_Sensors/blob/master/Python/Examples/EasyLightColorSensor.py>`__.

.. literalinclude:: ../../../Python/Examples/EasyLightColorSensor.py
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
