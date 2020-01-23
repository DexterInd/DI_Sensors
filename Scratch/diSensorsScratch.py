#!/usr/bin/env python
from __future__ import print_function
from __future__ import division

import time
import re
import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
dilogger = logging.getLogger("Sensors")

try:
    from di_sensors import easy_light_color_sensor
except:
    dilogger.debug("Cannot find light_color_sensor library")

try: 
    from di_sensors import easy_line_follower
except:
    dilogger.debug("Cannot find easy_line_follower library")

try: 
    from di_sensors import easy_temp_hum_press
except:
    dilogger.debug("Cannot find easy_temp_hum_press library")

scratch_lightcolor = None
scratch_linefollower = None
scratch_thp = None


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

# THP SENSOR
regexthp = "(^\s*(i2c)?\s*(temp)|(pressure)|(humidity)|(thp)\s*$)"

# ALL SENSORS
regexdisensors = "(" + \
                 regexlightcolor + ")|(" + \
                 regexlinefollower + ")|(" + \
                 regexthp + ")"

compiled_disensors = re.compile(regexdisensors, re.IGNORECASE)

def detect_light_color_sensor():
    global scratch_lightcolor
    try:
        # setting led_state to True just to give feedback to the user.
        scratch_lightcolor = easy_light_color_sensor.EasyLightColorSensor(led_state = True)
        dilogger.info("Light Color Sensor is detected")
        try:
            ''' attempt to broadcast commands'''
            s.broadcast('color')
            s.broadcast('rgb')
            s.broadcast('light')
        except:
            ''' no big deal at this stage '''
            pass
    except:
        dilogger.debug("Light Color Sensor not found")

def detect_line_follower():
    # force line follower to I2C port for now
    global scratch_linefollower
    try:
        scratch_linefollower = easy_line_follower.EasyLineFollower()
        dilogger.info("Line Follower is detected")
        try:
            s.broadcast('line')
        except:
            pass
    except:
        dilogger.debug("Line Follower not found")

def detect_thp():
    # force THP sensor to I2C port for now
    global scratch_thp
    try:
        scratch_thp = easy_temp_hum_press.EasyTHPSensor()
        dilogger.info("THP is detected")
        try:
            s.broadcast('temp')
            s.broadcast('humidity')
            s.broadcast('pressure')
            s.broadcast('thp')
        except:
            pass
    except Exception as e:
        dilogger.debug("THP not found")
        dilogger.debug(e)
        pass

def detect_all():
    detect_light_color_sensor()
    detect_line_follower()
    detect_thp()

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
    dilogger.debug ("handleDiSensors Rx: {}".format(msg))
    
    retdict = {}
    
    regObj = compiled_disensors.match(msg)
    if regObj == None:
        dilogger.info ("DI Sensors: Command %s is not recognized" % (msg))
        return None
    else:
        dilogger.debug ("matching done")
    
    if regObj:
        dilogger.debug (regObj.groups())

        # handling a light color sensor
        port = regObj.group(1)  # port nb goes from 0 to 3 from now on
        dilogger.debug("Port is %s" % port)

        # which method of the light color sensor is requested
        color_cmd = regObj.group(4)
        rgb_cmd = regObj.group(5)
        light_cmd = regObj.group(6)
        line_cmd = regObj.group(7)
        temp_cmd = regObj.group(14)
        pressure_cmd = regObj.group(15)
        humidity_cmd = regObj.group(16)
        thp_cmd = regObj.group(17)

        # don't use logger here as many of the arguments are None
        # and it crashes the logger
        print(color_cmd, rgb_cmd, light_cmd, line_cmd)
        print(temp_cmd, pressure_cmd, humidity_cmd, thp_cmd)

    else:
        dilogger.info( "DI Sensors: unknown regex error ")
        return None

    retdict = {}

    if color_cmd != None:
        # detecting the light color sensor as needed allows for hotplugging
        if scratch_lightcolor == None:
            detect_light_color_sensor()
        if scratch_lightcolor != None:
            dilogger.debug("Query color command")
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
                dilogger.info("color_cmd failed: ",e)
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
            dilogger.debug ("Query rgb values")
            try:
                red, green, blue = scratch_lightcolor.safe_rgb()
                if red != -1 and green != -1 and blue != -1:
                    retdict["rgb status"] = "ok"
            except Exception as e:
                dilogger.info("rgb_cmd failed ")
                dilogger.info(str(e))
                red, green, blue = [-1,-1,-1]
                scratch_lightcolor = None
                retdict["rgb status"] = "sensor not found"

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
                dilogger.debug("Query light value")
                scratch_lightcolor.set_led(False, True)
                time.sleep(0.01)
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
                dilogger.info("light_cmd failed: " + str(e) )
                scratch_lightcolor = None
                retdict["light status"] = "sensor not found"
        else:
            retdict["light status"] = "sensor not found"

    elif line_cmd != None:
        dilogger.debug("Found line follower cmd")
        if not scratch_linefollower:
            detect_line_follower()

        try:
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
                retdict["line status"] = "Oops! Could not find the line follower"
        except Exception as e:
            retdict["line status"] = "Oops! Could not read the line follower" 
            dilogger.info(str(e) )

    elif thp_cmd or temp_cmd or pressure_cmd or humidity_cmd:
        ''' any THP cmd '''
        try: 
            if not scratch_thp:
                detect_thp()
            if temp_cmd or thp_cmd :
                ''' temperature sensor'''
                dilogger.debug("temperature sensor")
                retdict["temperature (C)"] = scratch_thp.safe_celsius()
                retdict["temperature (F)"] = scratch_thp.safe_fahrenheit()

            if pressure_cmd or thp_cmd:
                ''' pressure sensor '''
                retdict["pressure (Pa)"] = scratch_thp.safe_pressure()

            if humidity_cmd or thp_cmd:
                ''' humidity sensor '''
                retdict["humidity (%)"] = scratch_thp.safe_humidity()

            retdict["THP Status"] = "ok"

        except Exception as e:
            retdict["THP Status"] = "Oops! Could not read the THP sensor" 
            dilogger.info(str(e))

    return (retdict)

def broadcast(in_str):
    global s
    if s == None:
        s = scratch.Scratch()
    try:
        s.broadcast(in_str)
    except:
        dilogger.debug("failed broadcasting")

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
            detect_all()
        
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
            dilogger.debug("Rx:{}".format(msg))
         
            if isDiSensorsMsg(msg):
                sensors = handleDiSensors(msg)
                if sensors != None:
                    s.sensorupdate(sensors)
                
        except KeyboardInterrupt:
            running= False
            dilogger.info ("DI Sensors Scratch: Disconnected from Scratch")
            break
        except (scratch.scratch.ScratchConnectionError,NameError) as e:
            while True:
                #thread1.join(0)
                dilogger.info ("DI Sensors Scratch: Scratch connection error, Retrying")
                time.sleep(5)
                try:
                    s = scratch.Scratch()
                    s.broadcast('READY')
                    dilogger.info ("DI Sensors Scratch: Connected to Scratch successfully")
                    break
                except scratch.ScratchError:
                    dilogger.info ("DI Sensors Scratch: Scratch is either not opened or remote sensor connections aren't enabled\n..............................\n")
        except Exception as e:
            dilogger.info ("DI Sensors Scratch: Error %s" % e	)
