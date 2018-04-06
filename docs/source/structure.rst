.. _structure-chapter:

###########################################
On Library & Hardware
###########################################

============
Requirements
============

Before you check the API for the DI-Sensors, please make sure you have the ``DI-Sensors`` package installed. You can do this by checking with ``pip`` by typing the following command.

.. code-block:: bash

   pip show DI-Sensors

Or you can check by trying to import the package in a Python console the following way:

.. code-block:: python

   import di_sensors

If there's nothing to be shown when ``pip show``-ing or you get an import error on the :py:mod:`di_sensors` package, then please check the :ref:`Getting Started <getting-started-chapter>` section and follow the instructions.

.. _hardware-interface-section:

==================
Hardware interface
==================

Instantiating the :ref:`4 sensors<getting-started-chapter>` in Python is a matter of choosing the right bus. Thus, there are 3 buses to choose from, depending on the context:

   * The ``"RPI_1"`` bus - this bus can be used on all 4 platforms we have (the GoPiGo3, GoPiGo, BrickPi3 & GrovePi). This bus corresponds to the ``"I2C"`` port.
   * The ``"GPG3_AD1"``/``"GPG3_AD2"`` buses - these buses can **only** be used on the GoPiGo3 platform. The advantage of using these ones is that the interface between the Raspberry Pi and the sensor is more stable. These buses correspond to the ``"AD1"`` and ``"AD2"`` ports of the GoPiGo3.

.. important::

   These notations for ports (``"RPI_1"``, ``"GPG3_AD1"`` and ``"GPG3_AD2"``) are only required for classes that *don't start* with the **Easy** word,
   specifically for:

   * :py:class:`~di_sensors.distance_sensor.DistanceSensor`
   * :py:class:`~di_sensors.inertial_measurement_unit.InertialMeasurementUnitSensor`
   * :py:class:`~di_sensors.light_color_sensor.LightColorSensor`
   * :py:class:`~di_sensors.temp_hum_press.TempHumPress`

   If you choose to use a sensor library *that starts* with the **Easy** word, you can use the same notations as those used and mentioned in the GoPiGo3's :ref:`documentation <gopigo3:hardware-ports-section>`, such as:

   * ``"I2C"`` instead of ``"RPI_1"``.
   * ``"AD1/AD2"`` instead of ``"GPG3_AD1/GPG3_AD2"``.

For seeing where the ``"AD1"``/``"AD2"`` are located on the GoPiGo3, please check the GoPiGo3's :ref:`documentation <gopigo3:hardware-ports-section>`.

==================
Library Structure
==================

------------------
Classes Short-List
------------------

The classes that are more likely to be of interest are graphically displayed shortly after this. In this graphic you can also notice inheritance links
between different classes. We can notice 3 groups of classes:

* Those that start with the **Easy** word in them and are easier to use and may provide some high-level functionalities.
* Those that don't start with the **Easy** word and yet are related to those that are. These are generally intented for power users.
* Those that look like they might represent a model number (that belong to modules such as :py:mod:`di_sensors.VL53L0X`, :py:mod:`di_sensors.BME280`, etc).
  These are intented for those who want to extend the functionalities of our library and are not documented here.

.. inheritance-diagram::
   di_sensors.easy_distance_sensor
   di_sensors.distance_sensor
   di_sensors.easy_inertial_measurement_unit
   di_sensors.easy_temp_hum_press
   di_sensors.inertial_measurement_unit
   di_sensors.easy_light_color_sensor
   di_sensors.light_color_sensor
   di_sensors.easy_mutex
   di_sensors.temp_hum_press
   di_sensors.VL53L0X
   di_sensors.BME280
   di_sensors.BNO055
   di_sensors.PCA9570
   di_sensors.TCS34725

.. note::

   Since this is an interactive graphic, you can click on the displayed classes and it'll take you to the documentation of a given class, if provided.

--------------------
Functions Short-List
--------------------

Here's a short summary of all classes and methods. There's a list going on for each class. We first start off by listing the **Easy** classes/methods
and then we end up showing the classes/methods for power users.
In this short summary, we're not covering the low-level classes that are not even documented in this documentation.

^^^^^^^^^^^^^^^^^^^^^^^^^^^
Easy - TempHumPress
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autosummary::

   di_sensors.easy_temp_hum_press.EasyTHPSensor
   di_sensors.easy_temp_hum_press.EasyTHPSensor.__init__
   di_sensors.easy_temp_hum_press.EasyTHPSensor.safe_celsius
   di_sensors.easy_temp_hum_press.EasyTHPSensor.safe_fahrenheit
   di_sensors.easy_temp_hum_press.EasyTHPSensor.safe_pressure
   di_sensors.easy_temp_hum_press.EasyTHPSensor.safe_humidity


^^^^^^^^^^^^^^^^^^^^
Easy - Light & Color
^^^^^^^^^^^^^^^^^^^^

.. autosummary::

   di_sensors.easy_light_color_sensor.EasyLightColorSensor
   di_sensors.easy_light_color_sensor.EasyLightColorSensor.__init__
   di_sensors.easy_light_color_sensor.EasyLightColorSensor.translate_to_hsv
   di_sensors.easy_light_color_sensor.EasyLightColorSensor.safe_raw_colors
   di_sensors.easy_light_color_sensor.EasyLightColorSensor.safe_rgb
   di_sensors.easy_light_color_sensor.EasyLightColorSensor.guess_color_hsv

^^^^^^^^^^^^^^^^^^^^
Easy - Distance
^^^^^^^^^^^^^^^^^^^^

.. autosummary::

   di_sensors.easy_distance_sensor.EasyDistanceSensor
   di_sensors.easy_distance_sensor.EasyDistanceSensor.__init__
   di_sensors.easy_distance_sensor.EasyDistanceSensor.read_mm
   di_sensors.easy_distance_sensor.EasyDistanceSensor.read
   di_sensors.easy_distance_sensor.EasyDistanceSensor.read_inches

^^^^^^^^^^^^^^^^^^^^
Easy - IMU
^^^^^^^^^^^^^^^^^^^^

.. autosummary::

   di_sensors.easy_inertial_measurement_unit.EasyIMUSensor
   di_sensors.easy_inertial_measurement_unit.EasyIMUSensor.__init__
   di_sensors.easy_inertial_measurement_unit.EasyIMUSensor.reconfig_bus
   di_sensors.easy_inertial_measurement_unit.EasyIMUSensor.safe_calibrate
   di_sensors.easy_inertial_measurement_unit.EasyIMUSensor.safe_calibration_status
   di_sensors.easy_inertial_measurement_unit.EasyIMUSensor.convert_heading
   di_sensors.easy_inertial_measurement_unit.EasyIMUSensor.safe_read_euler
   di_sensors.easy_inertial_measurement_unit.EasyIMUSensor.safe_read_magnetometer
   di_sensors.easy_inertial_measurement_unit.EasyIMUSensor.safe_north_point

^^^^^^^^^^^^^^^^^^^^^^^^^^^
TempHumPress
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autosummary::

   di_sensors.temp_hum_press.TempHumPress
   di_sensors.temp_hum_press.TempHumPress.__init__
   di_sensors.temp_hum_press.TempHumPress.get_temperature_celsius
   di_sensors.temp_hum_press.TempHumPress.get_temperature_fahrenheit
   di_sensors.temp_hum_press.TempHumPress.get_pressure
   di_sensors.temp_hum_press.TempHumPress.get_humidity
   di_sensors.temp_hum_press.TempHumPress.get_humidity

^^^^^^^^^^^^^^^^^^^^
Light & Color
^^^^^^^^^^^^^^^^^^^^

.. autosummary::

   di_sensors.light_color_sensor.LightColorSensor
   di_sensors.light_color_sensor.LightColorSensor.__init__
   di_sensors.light_color_sensor.LightColorSensor.set_led
   di_sensors.light_color_sensor.LightColorSensor.get_raw_colors

^^^^^^^^^^^^^^^^^^^^
Distance
^^^^^^^^^^^^^^^^^^^^

.. autosummary::

   di_sensors.distance_sensor.DistanceSensor
   di_sensors.distance_sensor.DistanceSensor.__init__
   di_sensors.distance_sensor.DistanceSensor.start_continuous
   di_sensors.distance_sensor.DistanceSensor.read_range_continuous
   di_sensors.distance_sensor.DistanceSensor.read_range_single
   di_sensors.distance_sensor.DistanceSensor.timeout_occurred

^^^^^^^^^^^^^^^^^^^^
IMU
^^^^^^^^^^^^^^^^^^^^

.. autosummary::

   di_sensors.inertial_measurement_unit.InertialMeasurementUnit
   di_sensors.inertial_measurement_unit.InertialMeasurementUnit.__init__
   di_sensors.inertial_measurement_unit.InertialMeasurementUnit.read_euler
   di_sensors.inertial_measurement_unit.InertialMeasurementUnit.read_magnetometer
   di_sensors.inertial_measurement_unit.InertialMeasurementUnit.read_gyroscope
   di_sensors.inertial_measurement_unit.InertialMeasurementUnit.read_accelerometer
   di_sensors.inertial_measurement_unit.InertialMeasurementUnit.read_linear_acceleration
   di_sensors.inertial_measurement_unit.InertialMeasurementUnit.read_gravity
   di_sensors.inertial_measurement_unit.InertialMeasurementUnit.read_quaternion
   di_sensors.inertial_measurement_unit.InertialMeasurementUnit.read_temperature


.. _distance sensor: https://www.dexterindustries.com/shop/distance-sensor/
.. _imu sensor: https://www.dexterindustries.com/shop/imu-sensor/
.. _inertialmeasurementunit sensor: https://www.dexterindustries.com/shop/imu-sensor/
.. _light color sensor: https://www.dexterindustries.com/shop/light-color-sensor/
.. _temperature humidity pressure sensor: https://www.dexterindustries.com/shop/temperature-humidity-pressure-sensor/
