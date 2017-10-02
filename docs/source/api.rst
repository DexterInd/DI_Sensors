.. _api-chapter:

##############
API DI-Sensors
##############

============
Requirements
============

Before you check the API for the DI-Sensors, please make sure you have the ``DI-Sensors`` package installed. You can do this by checking with ``pip`` by typing the following command.

.. code-block:: bash

   pip show DI-Sensors

If there's nothing to be shown, then please check the :ref:`Getting Started <getting-started-chapter>` section and follow the instructions.

.. _hardware-interface-section:

==================
Hardware interface
==================

Instantiating the :ref:`4 sensors<getting-started-chapter>` in Python is a matter of choosing the right bus. Thus, there are 3 buses to choose from, depending on the context:

    * The ``"RPI_1"`` bus - this bus can be used on all 4 platforms we have (the GoPiGo3, GoPiGo, BrickPi3 & GrovePi). This bus corresponds to the ``"I2C"`` port.
    * The ``"GPG3_AD1"``/``"GPG3_AD2"`` buses - these buses can **only** be used on the GoPiGo3 platform. The advantage of using these ones is that the interface between the Raspberry Pi and the sensor is more stable. These buses correspond to the ``"AD1"`` and ``"AD2"`` ports of the GoPiGo3.

For seeing where the ``"AD1"``/``"AD2"`` are located on the GoPiGo3, please check the GoPiGo3's `documentation <http://gopigo3.readthedocs.io/en/latest>`__.

==============
DistanceSensor
==============

.. autoclass:: di_sensors.distance_sensor.DistanceSensor
   :members:
   :special-members:
   :exclude-members: __weakref__

================
LightColorSensor
================

.. autoclass:: di_sensors.light_color_sensor.LightColorSensor
   :members:
   :special-members:
   :exclude-members: __weakref__

================
LightColorSensor
================

.. autoclass:: di_sensors.light_color_sensor.LightColorSensor
  :members:
  :special-members:
  :exclude-members: __weakref__


.. _distance sensor: https://www.dexterindustries.com/shop/distance-sensor/
.. _light color sensor: https://www.dexterindustries.com/shop/light-color-sensor/
