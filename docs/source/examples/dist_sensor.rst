.. _examples-distance-sensor:

#########################
Using the Distance Sensor
#########################

*************
Basic Example
*************

Before going to the more advanced example program of using the `Distance Sensor`_, we're going to give an example of the easiest way to read from the sensor.

The following code snippet reads values off of the `Distance Sensor`_ and prints them iteratively in the console. As you'll see, this is far easier than the
following examples, which are more complex to use, but have a more granular control over the device.

In this example program, connect the `Distance Sensor`_ to an I2C port on whichever platform (`GoPiGo3`_, `GrovePi`_ or `BrickPi3`_)
and then run the following script.

.. literalinclude:: ../../../Python/Examples/EasyDistanceSensor.py
  :language: python
  :lines: 14-

The source file for this example program can be found `here on github <https://github.com/DexterInd/DI_Sensors/blob/master/Python/Examples/EasyDistanceSensor.py>`__

***************
Continuous-mode
***************

Again, just like in the previous example program, connect the `Distance Sensor`_ to an I2C port on whichever platform before running the following script.

The advantage of this script over the ones in the following and previous sections is that the time taken for reading the distance
can be fine-tuned by the user - for instance, it can be made to run as fast as possible (to see how fast it can read see the API of :py:class:`~di_sensors.distance_sensor.DistanceSensor`) or it can be made to go very slow.
Each fine-tune has its benefits and disadvantages, so the user has to experiment with the sensor and determine what setting suits him best.

.. literalinclude:: ../../../Python/Examples/DistanceSensorContinuous.py
   :language: python
   :lines: 14-

The source code for this example program can be found `here on github <https://github.com/DexterInd/DI_Sensors/blob/master/Python/Examples/DistanceSensorContinuous.py>`__.

***********
Single-mode
***********

In this third example, we have the same physical arrangement as in the second one, the only difference being in how we communicate with the sensor.
This time, we take single-shot readings, which for the user is simpler than having to tune the distance sensor first and then read off of it. The only disadvantage is that
there's no fine-control over how fast the sensor is making the readings.

.. literalinclude:: ../../../Python/Examples/DistanceSensorSingleShot.py
   :language: python
   :lines: 14-

The source code for this example program can be found `here on github <https://github.com/DexterInd/DI_Sensors/blob/master/Python/Examples/DistanceSensorSingleShot.py>`__.

**************
Console Output
**************

All 3 example scripts described in this chapter should have a console output similar to what we have next.

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
