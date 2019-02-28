.. _api-chapter:

###########################################
API DI-Sensors - Basic
###########################################

==================
EasyDistanceSensor
==================

.. autoclass:: di_sensors.easy_distance_sensor.EasyDistanceSensor
   :members:
   :show-inheritance:
   :special-members:
   :exclude-members: __weakref__

====================
EasyLightColorSensor
====================

.. autoclass:: di_sensors.easy_light_color_sensor.EasyLightColorSensor
   :members:
   :show-inheritance:
   :special-members:
   :exclude-members: __weakref__

=============
EasyIMUSensor
=============

.. autoclass:: di_sensors.easy_inertial_measurement_unit.EasyIMUSensor
   :members:
   :show-inheritance:
   :special-members:
   :exclude-members: __weakref__

==============
EasyTHPSsensor
==============

.. autoclass:: di_sensors.easy_temp_hum_press.EasyTHPSensor
  :members:
  :show-inheritance:
  :special-members:
  :exclude-members: __weakref__

================
EasyLineFollower
================

.. autoclass:: di_sensors.easy_line_follower.EasyLineFollower
  :members:
  :show-inheritance:
  :special-members:
  :exclude-members: __weakref__

.. warning::

  The Line Follower class was originally held in :py:mod:`easysensors` module of the GoPiGo3 library, but has been moved here.
  The :py:meth:`easygopigo3.EasyGoPiGo3.init_line_follower` method now returns an object of the 
  :py:class:`~di_sensors.easy_line_follower.EasyLineFollower` class instead of instantiating the original Line Follower class from 
  :py:mod:`easysensors` module.

  In order to prevent breaking others' code, we kept the support for the older methods that are soon-to-be-deprecated in :py:class:`~di_sensors.easy_line_follower.EasyLineFollower` class.
  The mapping between the old methods and the new ones is as follows: 

    1. :py:meth:`~di_sensors.easy_line_follower.EasyLineFollower.read_raw_sensors` <=> :py:meth:`~di_sensors.easy_line_follower.EasyLineFollower.read`
    2. :py:meth:`~di_sensors.easy_line_follower.EasyLineFollower.read_binary` <=> :py:meth:`~di_sensors.easy_line_follower.EasyLineFollower.position_01`
    3. :py:meth:`~di_sensors.easy_line_follower.EasyLineFollower.read_position` <=> :py:meth:`~di_sensors.easy_line_follower.EasyLineFollower.position`
    4. :py:meth:`~di_sensors.easy_line_follower.EasyLineFollower.read_position_str` <=> :py:meth:`~di_sensors.easy_line_follower.EasyLineFollower.position_bw`
    5. :py:meth:`~di_sensors.easy_line_follower.EasyLineFollower.get_white_calibration` <=> :py:meth:`~di_sensors.easy_line_follower.EasyLineFollower.set_calibration` ``("white")``
    6. :py:meth:`~di_sensors.easy_line_follower.EasyLineFollower.get_black_calibration` <=> :py:meth:`~di_sensors.easy_line_follower.EasyLineFollower.set_calibration` ``("black")``

.. _distance sensor: https://www.dexterindustries.com/shop/distance-sensor/
.. _light color sensor: https://www.dexterindustries.com/shop/light-color-sensor/
.. _temperature humidity pressure sensor: https://www.dexterindustries.com/shop/temperature-humidity-pressure-sensor/
.. _inertialmeasurementunit sensor: https://www.dexterindustries.com/shop/imu-sensor/
.. _github repo: https://github.com/DexterInd/DI_Sensors
.. _gopigo3: https://www.dexterindustries.com/shop/gopigo3-robot-base-kit/
