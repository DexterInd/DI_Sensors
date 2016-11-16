import logging
import sys
import time
import BNO055
import gopigo
import atexit
atexit.register(gopigo.stop)
bno = BNO055.BNO055()

if not bno.begin(mode=BNO055.OPERATION_MODE_NDOF):
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

status, self_test, error = bno.get_system_status()
print('System status: {0}'.format(status))
print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
# Print out an error if system status is in error mode.
if status == 0x01:
    print('System error: {0}'.format(error))
    print('See datasheet section 4.3.59 for the meaning.')

def get_euler_from_bno():
    for i in range (10):
        flag=0
        heading, roll, pitch = bno.read_euler()
        fact=1.0
        if heading >360*fact or heading < 0:
            flag=1
        if roll >90*fact or roll < -90*fact:
            flag=1
        if pitch >180*fact or pitch < -180*fact: 
            flag=1
        if flag !=1:
            return (heading, roll, pitch)
    
start_flag=0
start_heading=0

#First move forward
moving_forward_state=1
turning_state=0
turning_start=0
for i in range (50):
    heading, roll, pitch = get_euler_from_bno()
    
while True:
    heading, roll, pitch = get_euler_from_bno()
    print('1Heading={0:0.2F},'.format(heading)) 
    if heading <360 and heading > 0:
        if start_flag==0:
            start_flag=1
            start_heading=heading
            target_heading=start_heading+90.0
            if target_heading > 360.0:
                target_heading-=360
            #Starting speed
            time.sleep(5)
            gopigo.set_speed(150)
        else:
            if moving_forward_state:
                print "---------------------------->Turning state"
                gopigo.fwd()
                time.sleep(3)
                gopigo.stop()
                moving_forward_state=0
                turning_state=1
                print "Moving Forward"
            elif turning_state:
                if turning_start==0:
                    print "---------------------------->Turning state"
                    #Starting speed
                    time.sleep(2)
                    print('Start Heading={0:0.2F},Targt Heading={1:0.2F},Current Heading={2:0.2F},Diff={3:0.2F}'.format(start_heading,target_heading,heading,target_heading-heading)) 
                    gopigo.set_speed(60)
                    
                    start_heading=heading
                    target_heading=start_heading+90.0
                        
                    if target_heading < start_heading:
                        target_heading+=360.0
                    turning_start=1
                    gopigo.right_rot()
                else:
                    if target_heading >360:
                        if heading <270:
                            heading+=360
                if target_heading-heading<5:
                    print "------------------------------------------->target reached"
                    gopigo.stop() 
                    turning_start=0 
                    turning_stat=0
                    moving_forward_state=1
                    start_flag=0
        print('Start Heading={0:0.2F},Targt Heading={1:0.2F},Current Heading={2:0.2F},Diff={3:0.2F}'.format(start_heading,target_heading,heading,target_heading-heading)) 
    
   
