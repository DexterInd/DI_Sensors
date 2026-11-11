#!/usr/bin/env python
#
# https://www.dexterindustries.com
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# Python example program for the Dexter Industries Temperature Humidity Pressure Sensor

# do the import stuff
from di_sensors.easy_distance_sensor import EasyDistanceSensor
from time import time, sleep
from threading import Thread, Event, get_ident

# instantiate the distance object
try:
    my_sensor = EasyDistanceSensor(use_mutex = True)
except OSError as e:
    print(f"Failed to initialize distance sensor: {e}")
    print("Check that the sensor is connected and I2C is enabled (sudo raspi-config).")
    raise SystemExit(1)

start_time = time()
runtime = 10.0
# create an event object for triggering the "shutdown" of each thread
stop_event = Event()

# target function for each thread
def readingSensor():
    while not stop_event.is_set():
        thread_id = get_ident()
        try:
            distance = my_sensor.read()
            print(f"Thread ID = {thread_id} with distance value = {distance}")
        except OSError as e:
            print(f"Thread ID = {thread_id}: I2C read error: {e}")
        sleep(0.05)

# create an object for each thread
thread1 = Thread(target = readingSensor)
thread2 = Thread(target = readingSensor)

# and then start them

thread1.start()
print(f"Starting First Thread with ID = {thread1.ident}")
sleep(2) # let the first thread run for a bit before starting the second one, just to show that they can be started at different times
thread2.start()
print(f"**** Starting Second Thread with ID = {thread2.ident}")

try:
    # let it run for [runtime] seconds
    while time() - start_time <= runtime:
        sleep(0.1)
except KeyboardInterrupt:
    print("\nInterrupted - shutting down...")
finally:
    # signal threads to stop and wait for them
    stop_event.set()
    thread1.join()
    thread2.join()
    # reset sensor back to default address so the next run can find it
    my_sensor.close()
    print("Sensor closed.")
