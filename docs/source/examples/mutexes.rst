#############
Using Mutexes
#############

In this section, we are showing how handy mutexes are when we're trying to access the same resource (a device, for instance a `Distance Sensor`_)
simultaneously from multiple threads. All :ref:`Easy classes <api-chapter>` are thread-safe - what one has to do is to activate the use of mutexes by passing a boolean
parameter to each of the classes' constructor.

In the following example program, 2 threads are accessing the resource of an :py:class:`~di_sensors.easy_distance_sensor.EasyDistanceSensor` object.
``use_mutex`` parameter is set to ``True`` so that the resource can be accessed from multiple threads/processes (this is what we would call a thread-safe class).
Each of these 2 threads run for ``runtime`` seconds - we didn't make it so one can stop the program while it's running, because that would have been more complex.

Without the mutex mechanism, accessing the same resource from multiple processes/threads would not be possible.

.. literalinclude:: ../../../Python/Examples/EasyDistanceSensorMutexes.py
  :language: python
  :lines: 14-

.. important::

   There was no need to use mutexes in the above example, but for the sake of an example, it is a good thing. The idea is that CPython's implementation
   has what it's called a **GIL** (*Global Interpreter Lock*) and this only allows one thread to run at once, which is a skewed way of envisioning how threads work,
   but it's the reality in Python still. Ideally, a thread can run concurrently with another one. You can read more on the :term:`Global Interpreter Lock here<python:global interpreter lock>`.

   Still, the implementation we have with mutexes proves to be useful when one wants to launch multiple processes at a time - at that moment, we can talk of true concurrency.
   This can happen when multiple instances of Python scripts are launched and when each process tries to access the same resource as the other one.

The output on the console should look like this - the thread IDs don't mean anything and they are merely just a number used to identify threads.

.. code-block:: bash

  Thread ID = 1883501680 with distance value = 44
  Thread ID = 1873802352 with distance value = 44
  Thread ID = 1873802352 with distance value = 44
  Thread ID = 1883501680 with distance value = 44
  Thread ID = 1873802352 with distance value = 46
  Thread ID = 1883501680 with distance value = 46
  Thread ID = 1873802352 with distance value = 45
  Thread ID = 1883501680 with distance value = 45
  Thread ID = 1883501680 with distance value = 44
  Thread ID = 1873802352 with distance value = 44
  Thread ID = 1883501680 with distance value = 45
  Thread ID = 1873802352 with distance value = 45

.. _distance sensor: https://www.dexterindustries.com/shop/distance-sensor/
