.. _examples-distance-sensor:

#########################
Using the Distance Sensor
#########################

***************
Continuous-mode
***************

In this example program, connect the `Distance Sensor`_ to an I2C port on whichever platform (`GoPiGo3`_, `GrovePi`_ or `BrickPi3`_)
and then run the following script.

The advantage of this script over the one in the following section is that the time taken for reading the distance
can be fine-tuned by the user - for instance, it can be made to run as fast as possible (see the API to see how fast it can read) or it can be made to go very slow.
Each fine-tune has its benefits and disadvantages, so the user has to experiment with the sensor and determine what setting suits him best.

.. literalinclude:: ../../../Python/Examples/DistanceSensorContinuous.py
   :language: python
   :lines: 14-

The source code for this example program can be found `here on github <https://github.com/DexterInd/DI_Sensors/blob/master/Python/Examples/DistanceSensorContinuous.py>`__.

Here's how the console output of the script should look like:

***********
Single-mode
***********

In this second example, we have the same physical arrangement as in the first one, the only difference being in how we communicate with the sensor.
This time, we take single-shot readings, which for the user is the simplest way of reading data off the sensor. The only disadvantage is that
there's no fine-control over how fast the sensor is making the readings.

.. literalinclude:: ../../../Python/Examples/DistanceSensorSingleShot.py
   :language: python
   :lines: 14-

The source code for this example program can be found `here on github <https://github.com/DexterInd/DI_Sensors/blob/master/Python/Examples/DistanceSensorSingleShot.py>`__.

**************
Console Output
**************

Both example scripts described in this chapter should have a console output similar to what we have next.

.. code-block:: bash

  distance from object: 419 mm
  distance from object: 454 mm
  distance from object: 452 mm
  distance from object: 490 mm
  distance from object: 501 mm
  distance from object: 8190 mm
  distance from object: 1650 mm
  distance from object: 1678 mm
  distance from object: 1638 mm
  distance from object: 1600 mm

.. _distance sensor: https://www.dexterindustries.com/shop/distance-sensor/
.. _gopigo3: https://www.dexterindustries.com/gopigo3/
.. _grovepi: https://www.dexterindustries.com/grovepi/
.. _brickpi3: https://www.dexterindustries.com/brickpi/
