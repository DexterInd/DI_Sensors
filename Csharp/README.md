# .NET Core IoT implementation for Dexter Industries Sensors

You will find a full implantation of  Dexter Industries Sensors on [.NET Core IoT repository](https://github.com/dotnet/iot). You will be able to program GoPiGo, GrovePi, and BrickPi using C#. The full documentation and example is located into the main repository.

.NET Core is open source. .NET Core is best thought of as 'agile .NET'. Generally speaking it is the same as the Desktop .NET Framework distributed as part of the Windows operating system, but it is a cross platform (Windows, Linux, macOS) and cross architecture (x86, x64, ARM) subset that can be deployed as part of the application (if desired), and thus can be updated quickly to fix bugs or add features. It is a perfect fit for boards like Raspberry running Raspbian. Check the [.NET Core IoT documentation](https://github.com/dotnet/iot/tree/master/Documentation) if you are not familiar with .NET Core.

Compatibility
-------------

The following Grove compatible devices are supported in .NET Core IoT:

* Dexter Industries:
  * **[Distance Sensor](https://www.dexterindustries.com/shop/distance-sensor/)** - Distance Sensor for the GoPiGo, GrovePi, and BrickPi.  The distance sensor can be mounted to the GoPiGo Raspberry Pi robot with or without the servo package to enable rotation. The sensor detects distances from obstacles and objects, giving your robot the ability to navigate. You will find this code under [VL53L0X implementation](https://github.com/dotnet/iot/tree/master/src/devices/Vl53L0X). A [full sample](https://github.com/dotnet/iot/tree/master/src/devices/Vl53L0X/samples) is provided as well.

  * **[Inertial Measurement Unit Sensor](https://www.dexterindustries.com/shop/imu-sensor/)** - The IMU Sensor attaches to the GrovePi, GoPiGo and BrickPi to detect motion, orientation, and position of your robot. It has a compass, accelerometer, and gyroscope and allows you to build a BalanceBot. You will find this code under [BNO055 implementation](https://github.com/dotnet/iot/tree/master/src/devices/Bno055). A [full sample](https://github.com/dotnet/iot/tree/master/src/devices/Bno055/samples) is provided as well.

  * **[Light Color Sensor](https://www.dexterindustries.com/shop/light-color-sensor/)** - The Light & Color Sensor attaches to the GrovePi, GoPiGo and BrickPi to measure light levels and detect different colors. It can be used to build projects like a rubiks cube solver, weather station, or plant monitoring station. You will find this code under [Bmx280 implementation](https://github.com/dotnet/iot/tree/master/src/devices/Bmx280). A [full sample](https://github.com/dotnet/iot/tree/master/src/devices/Bmx280/samples) is provided as well. Please make sure you will use the BME280 implemnation. Usage is describe in the [example here](https://github.com/dotnet/iot/tree/master/src/devices/Bmx280/samples/Bme280.sample.cs). 

  * **[Temperature Humidity Pressure Sensor](https://www.dexterindustries.com/shop/temperature-humidity-pressure-sensor/)**- The Temperature Humidity and Pressure Sensor attaches to the GrovePi, GoPiGo and BrickPi to measure environmental conditions. It can be used to build projects like a classroom weather station or plant monitoring station. You will find this code under [BNO055 implementation](https://github.com/dotnet/iot/tree/master/src/devices/Bno055). A [full sample](https://github.com/dotnet/iot/tree/master/src/devices/Bno055/samples) is provided as well.
