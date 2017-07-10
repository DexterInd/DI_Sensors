#!/usr/bin/env python
#
# https://www.dexterindustries.com/
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# Python example program for the Dexter Industries Distance Sensor

from __future__ import print_function
from __future__ import division

import time
from DI_Sensors import distance_sensor

print("Example program for reading a Dexter Industries Distance Sensor on a GoPiGo3 AD1 port.")

ds = distance_sensor.DistanceSensor("GPG3_AD1")

while True:
    # read the distance as a single-shot sample
    print("%4dmm" % ds.read_range_single())
    if ds.timeout_occurred():
        print(" TIMEOUT")
