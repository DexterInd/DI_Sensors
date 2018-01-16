#!/usr/bin/env python
#
# https://www.dexterindustries.com
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# Python example program for the Dexter Industries Line Follower sensor

from __future__ import print_function
from __future__ import division

import time
from di_sensors import line_follower

print("Example program for reading a Dexter Industries Line Follower sensor on GPG3 AD1 port")

lf = line_follower.LineFollower(bus = "GPG3_AD1")

'''
cd ~/Dexter/DI_Sensors/Python
sudo python setup.py install

python ~/Dexter/DI_Sensors/Python/Examples/LineFollower.py

'''

print("Manufacturer     : %s" % lf.get_manufacturer())
print("Name             : %s" % lf.get_board())
print("Firmware Version : %d" % lf.get_version_firmware())

while True:
    # Read the line sensors values
    values = lf.read_sensors()
    str = ""
    for v in range(len(values)):
        str += "%.3f " % values[v]
    print(str)
    
    values = lf.read_sensors(lf.BOTH)
    str = ""
    for v in range(len(values)):
        str += "%.3f " % values[v]
    print(str)
    
    time.sleep(0.1)
