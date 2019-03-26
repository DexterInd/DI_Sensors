#!/usr/bin/env python
from __future__ import print_function
from __future__ import division

import time
import re
import sys

try:
    from di_sensors import easy_light_color_sensor
except:
    print("Cannot find light_color_sensor library")

try: 
    from di_sensors import easy_line_follower
except:
    print("Cannot find easy_line_follower library")

en_debug = 1
scratch_lightcolor = None
scratch_linefollower = None


# LIGHT COLOR SENSOR
# possible commands are:
# i2c color, i2c colour, color, colour
# i2c rgb, rgb
# i2c light, I2C lite, light, lite

# group 1 = i2c 
# group 2 = color
# group 3 = rgb
# group 4 = light
regexlightcolor = "^\s*(i2c)?\s*((colou?r)|(rgb)|(light|lite))\s*$"


# LINE FOLLOWER SENSOR
regexlinefollower = "(^\s*(i2c)?\s*(line)\s*$)"

# ALL SENSORS
regexdisensors = "("+ regexlightcolor+")|(" + regexlinefollower + ")"
compiled_disensors = re.compile(regexdisensors, re.IGNORECASE)

def detect_light_color_sensor():
    global scratch_lightcolor
    try:
        # setting led_state to True just to give feedback to the user.
        scratch_lightcolor = easy_light_color_sensor.EasyLightColorSensor(led_state = True)
        print("Light Color Sensor is detected")
    except:
        pass

def detect_line_follower():
    # force line follower to I2C port for now
    global scratch_linefollower
    try:
        scratch_linefollower = easy_line_follower.EasyLineFollower()
        print("Line Follower is detected")
    except:
        pass

def detect_all():
    detect_light_color_sensor()
    detect_line_follower()

def isDiSensorsMsg(msg):
    '''
    Is the msg supposed to be handled by Light Color Sensor or the Line Follower?
    Return: Boolean 
        True if valid for Light Color or Line Follower
        False otherwise
    '''
    retval = compiled_disensors.match(msg)
    
    if retval == None:
        return False
    else:
        return True


def handleDiSensors(msg):
    '''
    Scratch is sending a msg to a Light Color Sensor. 
    Use regex to validate it and take it apart
    '''
    global scratch_lightcolor
    if en_debug:
        print ("handleDiSensors Rx: {}".format(msg))
    
    retdict = {}
    
    regObj = compiled_disensors.match(msg)
    if regObj == None:
        print ("DI Sensors: Command %s is not recognized" % (msg))
        return None
    # else:
        # if en_debug:
            # print ("matching done")
    
    if regObj:
    #     print (regObj.groups())

        # handling a light color sensor
        port = regObj.group(1)  # port nb goes from 0 to 3 from now on
        # print("Port is %s" % port)

        # which method of the light color sensor is requested
        color_cmd = regObj.group(3)
        rgb_cmd = regObj.group(4)
        light_cmd = regObj.group(5)
        line_cmd = regObj.group(7)
        print(color_cmd, rgb_cmd, light_cmd, line_cmd)

    else:
        print( "DI Sensors: unknown regex error ")
        return None

    retdict = {}

    if color_cmd != None:
        # detecting the light color sensor as needed allows for hotplugging
        if scratch_lightcolor == None:
            detect_light_color_sensor()
        if scratch_lightcolor != None:
            # print("Query color command")
            try:
                scratch_lightcolor.set_led(True)
                color = scratch_lightcolor.safe_raw_colors()
                if color != [-1,-1,-1,-1]:
                    retdict["color"] = scratch_lightcolor.guess_color_hsv(color)[0]
                    retdict["color status"] = ""
                else:
                    # sensor got disconnected
                    retdict["color"] = "unknown"
                    scratch_lightcolor = None
                    retdict["color status"] = "sensor not found"
            except Exception as e:
                print("color_cmd failed: ",e)
                retdict["color"] = "unknown"
                scratch_lightcolor = None
                retdict["color status"] = "sensor not found"
        else:
            retdict["color status"] = "sensor not found"


    elif rgb_cmd != None:
        # detecting the light color sensor as needed allows for hotplugging
        if scratch_lightcolor == None:
            detect_light_color_sensor()
        if scratch_lightcolor != None:
            # print ("Query rgb values")
            try:
                red, green, blue = scratch_lightcolor.safe_rgb()
                if red != -1 and green != -1 and blue != -1:
                    # sensor got disconnected
                    red, green, blue = [-1,-1,-1]
                    scratch_lightcolor = None
                    retdict["rgb status"] = ""
            except Exception as e:
                print("rgb_cmd failed: ",e)
                red, green, blue = [-1,-1,-1]
                scratch_lightcolor = None
                retdict["rgb status"] = "sensor not found"

            # print(red, green, blue)
            retdict["rgb red"] = red
            retdict["rgb green"] = green
            retdict["rgb blue"] = blue
        else:
            retdict["rgb status"] = "sensor not found"

    elif light_cmd != None:
        # detecting the light color sensor as needed allows for hotplugging
        if scratch_lightcolor == None:
            detect_light_color_sensor()
        if scratch_lightcolor != None:
            try:
                # print("Query light value")
                scratch_lightcolor.set_led(False, True)
                _,_,_,a = scratch_lightcolor.safe_raw_colors()
                scratch_lightcolor.set_led(True)
                if a != -1:
                    retdict["light"]= int(a*100)  # return as a percent value
                    retdict["light status"] = "ok"
                else:
                    # sensor got disconnected
                    retdict["light"]=int(a)
                    scratch_lightcolor = None
                    retdict["light status"] = "sensor not found"
            except Exception as e:
                print("light_cmd failed: ", e)
                scratch_lightcolor = None
                retdict["light status"] = "sensor not found"
        else:
            retdict["light status"] = "sensor not found"

    elif line_cmd != None:
        # print("Found line follower cmd")
        if not scratch_linefollower:
            detect_line_follower()

        if scratch_linefollower:
            line_values = scratch_linefollower.read()
            estimated_position, lost_line = scratch_linefollower._weighted_avg(line_values)
            retdict["line position"] = scratch_linefollower._position(estimated_position, lost_line )
            retdict["line sensors bw"] = scratch_linefollower._bivariate_str(line_values)
            retdict["line number"] = scratch_linefollower.position_val()
            retdict["line sensor 1"] = line_values[0]
            retdict["line sensor 2"] = line_values[1]
            retdict["line sensor 3"] = line_values[2]
            retdict["line sensor 4"] = line_values[3]
            retdict["line sensor 5"] = line_values[4]
            if len(line_values) == 6:
                retdict["line sensor 6"] = line_values[5]
            retdict["line status"] = "ok"
        else:
            retdict["line status"] = "line follower not found"

    return (retdict)


# this is used when developing.
# the light color sensor is not supported as a standalone in Scratch

if __name__ == '__main__':
    
    #this import is only needed when run as standalone, which is not supported
    import scratch

    connected = 0	# This variable tells us if we're successfully connected.
    print( "Waiting for Scratch")

    while(connected == 0):
        startTime = time.time()
        try:
            s = scratch.Scratch()
            if s.connected:
                print ("DI Sensors Scratch: Connected to Scratch successfully")
            connected = 1	# We are succesfully connected!  Exit Away!
            # time.sleep(1)
        
        except scratch.ScratchError:
            arbitrary_delay = 10 # no need to issue error statement if at least 10 seconds haven't gone by.
            if (time.time() - startTime > arbitrary_delay):  
                print ("DI Sensors Scratch: Scratch is either not opened or remote sensor connections aren't enabled")

    try:
        s.broadcast('READY')
    except NameError:
        print ("DI Sensors Scratch: Unable to Broadcast")


    while True:
        try:
            m = s.receive()
            
            while m==None or m[0] == 'sensor-update' :
                m = s.receive()
            
            msg = m[1]
            if en_debug:
                print("Rx:{}".format(msg))
         
            if isDiSensorsMsg(msg):
                sensors = handleDiSensors(msg)
                if sensors != None:
                    s.sensorupdate(sensors)
                
        except KeyboardInterrupt:
            running= False
            print ("DI Sensors Scratch: Disconnected from Scratch")
            break
        except (scratch.scratch.ScratchConnectionError,NameError) as e:
            while True:
                #thread1.join(0)
                print ("DI Sensors Scratch: Scratch connection error, Retrying")
                time.sleep(5)
                try:
                    s = scratch.Scratch()
                    s.broadcast('READY')
                    print ("DI Sensors Scratch: Connected to Scratch successfully")
                    break
                except scratch.ScratchError:
                    print ("DI Sensors Scratch: Scratch is either not opened or remote sensor connections aren't enabled\n..............................\n")
        except Exception as e:
            print ("DI Sensors Scratch: Error %s" % e	)
