###########################################
API DI-Sensors - Advanced
###########################################

==============
DistanceSensor
==============

.. autoclass:: di_sensors.distance_sensor.DistanceSensor
   :members:
   :show-inheritance:
   :special-members:
   :exclude-members: __weakref__

================
LightColorSensor
================

.. autoclass:: di_sensors.light_color_sensor.LightColorSensor
   :members:
   :show-inheritance:
   :special-members:
   :exclude-members: __weakref__

=======================
InertialMeasurementUnit
=======================

.. autoclass:: di_sensors.inertial_measurement_unit.InertialMeasurementUnit
   :members:
   :show-inheritance:
   :special-members:
   :exclude-members: __weakref__

   .. automethod:: di_sensors.BNO055.BNO055.get_calibration_status

============
TempHumPress
============

.. autoclass:: di_sensors.temp_hum_press.TempHumPress
  :members:
  :show-inheritance:
  :special-members:
  :exclude-members: __weakref__

============
LineFollower
============

.. autoclass:: di_sensors.line_follower.LineFollower
   :members:
   :show-inheritance:
   :special-members:
   :exclude-members: __weakref__

.. autoclass:: di_sensors.line_follower.LineFollowerRed
   :members:
   :show-inheritance:
   :special-members:
   :exclude-members: __weakref__

========
More ...
========

If you wish to have a more granular control over the sensors' functionalities, then you should check the following submodules of the ``DI-Sensors`` package:

   * `di_sensors.BME280 <https://github.com/DexterInd/DI_Sensors/blob/master/Python/di_sensors/BME280.py>`_ - submodule for interfacing with the `Temperature Humidity Pressure Sensor`_.
   * `di_sensors.BNO055 <https://github.com/DexterInd/DI_Sensors/blob/master/Python/di_sensors/BNO055.py>`_ - submodule for interfacing with the `InertialMeasurementUnit Sensor`_.
   * `di_sensors.TCS34725 <https://github.com/DexterInd/DI_Sensors/blob/master/Python/di_sensors/TCS34725.py>`_ - submodule for interfacing with the `Light Color Sensor`_.
   * `di_sensors.VL53L0X <https://github.com/DexterInd/DI_Sensors/blob/master/Python/di_sensors/VL53L0X.py>`_ - submodule for interfacing with the `Distance Sensor`_.

All these submodules that are being referenced in this section were used for creating the :py:class:`~di_sensors.distance_sensor.DistanceSensor`,
:py:class:`~di_sensors.light_color_sensor.LightColorSensor`, :py:class:`~di_sensors.temp_hum_press.TempHumPress` and the :py:class:`~di_sensors.inertial_measurement_unit.InertialMeasurementUnit` classes.


.. _distance sensor: https://www.dexterindustries.com/shop/distance-sensor/
.. _light color sensor: https://www.dexterindustries.com/shop/light-color-sensor/
.. _temperature humidity pressure sensor: https://www.dexterindustries.com/shop/temperature-humidity-pressure-sensor/
.. _inertialmeasurementunit sensor: https://www.dexterindustries.com/shop/imu-sensor/
.. _line follower sensor (black board): https://www.dexterindustries.com/shop/line-follower-sensor/
.. _line follower sensor (red board): https://www.dexterindustries.com/product/line-follower-for-gopigo/
.. _github repo: https://github.com/DexterInd/DI_Sensors
