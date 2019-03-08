.. _examples-basic-lf:

#######################
Using the Line Follower
#######################

In order to run this example program, we need to have a `GoPiGo3`_ because bus ``"GPG3_AD1"`` is used in this case and it's specific to the `GoPiGo3`_ platform.
The ``"GPG3_AD1"`` bus translates to port ``"AD1"`` on the GoPiGo3, so the `IMU Sensor`_ has to be connected to port ``"AD1"``.

The default ``"RPI_1SW"`` bus could have been used, but since this is an example, let's do it with a `GoPiGo3`_.

This is the exact same scenarion as the one in :ref:`IMU sensor example <examples-imu-sensor>`.

The source file for this example program can be found `here on github <https://github.com/DexterInd/DI_Sensors/blob/master/Python/Examples/LineFollower.py>`__.

.. literalinclude:: ../../../Python/Examples/LineFollower.py
   :language: python
   :lines: 14-

The console output of this script should look like:

.. code-block:: bash

    Example program for reading a Dexter Industries Line Follower sensor on GPG3 AD1 port
    Manufacturer     : Dexter Industries
    Name             : Line Follower
    Firmware Version : 1
    0.031 0.044 0.051 0.038 0.033 0.017
    0.035 0.054 0.063 0.051 0.048 0.026
    0.048 0.065 0.075 0.061 0.059 0.034
    0.047 0.065 0.076 0.063 0.064 0.040
    0.063 0.080 0.096 0.091 0.091 0.071
    0.070 0.087 0.104 0.103 0.107 0.087
    0.070 0.088 0.107 0.103 0.108 0.090
    0.120 0.090 0.115 0.121 0.128 0.116
    0.283 0.089 0.121 0.141 0.177 0.196
    0.383 0.109 0.155 0.206 0.299 0.404
    0.454 0.159 0.185 0.250 0.396 0.340
    0.287 0.338 0.111 0.115 0.132 0.137
    0.443 0.208 0.268 0.132 0.109 0.079
    0.285 0.484 0.259 0.167 0.095 0.057
    0.589 0.200 0.268 0.176 0.091 0.051
    0.695 0.158 0.180 0.359 0.219 0.157
    0.625 0.095 0.152 0.369 0.227 0.069
    0.398 0.098 0.127 0.383 0.372 0.081
    0.698 0.111 0.128 0.720 0.902 0.193
    0.297 0.124 0.138 0.447 0.843 0.187
    0.104 0.146 0.180 0.392 0.960 0.291
    0.096 0.132 0.158 0.319 0.945 0.299
    0.094 0.128 0.152 0.376 0.935 0.249
    0.084 0.114 0.144 0.710 0.716 0.143
    0.065 0.095 0.567 0.617 0.149 0.157
    0.061 0.298 0.331 0.096 0.109 0.117
    0.275 0.239 0.102 0.112 0.144 0.170


Also, doing something more advanced with the line follower is possible by using the :py:class:`~di_sensors.easy_line_follower.EasyLineFollower` class. With an object of such type,
a estimated position of the black line can be returned and then feed this estimate into a PID controller. Consequently, a robot (such as the GoPiGo3) can be precisely controlled.

.. code-block:: python

    from di_sensors.easy_line_follower import EasyLineFollower
    from time import time, sleep

    setpoint = 0.5
    integralArea = 0.0
    previousError = 0.0
    motorBaseSpeed = 300
    loopTime = 1.0 / 100

    Kp = 0.0 # a value suitable for this component
    Ki = 0.0 # ditto
    Kd = 0.0 # ditto as above

    lf = EasyLineFollower()

    while True:
        start = time()
        pos, out_of_line = lf.read_sensors('weighted-avg')
        error = pos - setpoint

        integralArea += error
        correction = Kp * error + Ki * integralArea + Kd * (previousError - error)
        previousError = error

        motorA = motorBaseSpeed + correction
        motorB = motorBaseSpeed - correction

        # code for actuating the robot to follow the line
        # using the previously computed values for each motor
        
        # to make it run at certain frequency
        end = time()
        alreadySpent = end - start
        remainingTime = loopTime - alreadySpent
        if remainingTime > 0:
            sleep(remainingTime)


With something like the above code, you can make a pretty reliable control system for the line follower. 


.. _imu sensor: https://www.dexterindustries.com/shop/imu-sensor/
.. _gopigo3: https://www.dexterindustries.com/gopigo3/
.. _grovepi: https://www.dexterindustries.com/grovepi/
.. _brickpi3: https://www.dexterindustries.com/brickpi/
