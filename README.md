DI_Sensors [![Documentation Status](http://readthedocs.org/projects/di-sensors/badge/?version=master)](http://di-sensors.readthedocs.io/en/master/?badge=master)
============
Dexter Industries Sensors

Compatibility
-------------

The following Grove compatible devices are supported in Python:

* Dexter Industries:
  * **[Distance Sensor](https://www.dexterindustries.com/shop/distance-sensor/)** - Distance Sensor for the GoPiGo, GrovePi, and BrickPi.  The distance sensor can be mounted to the GoPiGo Raspberry Pi robot with or without the servo package to enable rotation.  The sensor detects distances from obstacles and objects, giving your robot the ability to navigate.

  * **[Inertial Measurement Unit Sensor](https://www.dexterindustries.com/shop/imu-sensor/)** - The IMU Sensor attaches to the GrovePi, GoPiGo and BrickPi to detect motion, orientation, and position of your robot. It has a compass, accelerometer, and gyroscope and allows you to build a BalanceBot.

  * **[Light Color Sensor](https://www.dexterindustries.com/shop/light-color-sensor/)** - The Light & Color Sensor attaches to the GrovePi, GoPiGo and BrickPi to measure light levels and detect different colors. It can be used to build projects like a rubiks cube solver, weather station, or plant monitoring station.

  * **[Temperature Humidity Pressure Sensor](https://www.dexterindustries.com/shop/temperature-humidity-pressure-sensor/)**- The Temperature Humidity and Pressure Sensor attaches to the GrovePi, GoPiGo and BrickPi to measure environmental conditions. It can be used to build projects like a classroom weather station or plant monitoring station.

* Grove:
  * RGB LCD


Installation
------------

In order to quick install the `DI_Sensors` repository, open up a terminal and type one of the 2 following commands:

1. For installing the python packages of the `DI_Sensors` with root privileges (except any other settings that can come with), use the following command:
```
sudo sh -c "curl -kL dexterindustries.com/update_sensors | bash"
```

2. For installing the python packages of the `DI_Sensors` without root privileges (except any other settings that can come with), use the following command:
```
curl -kL dexterindustries.com/update_sensors | bash
```
The same command can be used for updating the `DI_Sensors` to the latest version.

License
-------

Please review the [LICENSE.md] file for license information.

[LICENSE.md]: ./LICENSE.md
