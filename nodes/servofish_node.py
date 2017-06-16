#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Joy
import servofish
from time import time

lastsendtime=time()

send_interval = .5
#create the fish communication object
fish = servofish.ServoFish('/dev/ttyACM1',115200)

biasmax = 45#deg
biasmin = -45#deg
freqmax = 25#rad/s
freqmin = 0 #rad/s
ampmin = 0
ampmax = 45#deg


def joycallback(data):
    global lastsendtime
    freqcommand = (data.axes[1]+1)*freqmax/2
    biascommand = (data.axes[2])*biasmax
    ampcommand = (data.axes[3]+1)*ampmax/2
    if data.buttons[6]==1:
        fish.fishenable()
    else:
        fish.fishdisable()
    if ((time()-lastsendtime)>send_interval):
        fish.writeCommand(freqcommand,biascommand,ampcommand)
        print "time "+str(time())+" wrote: "+str(freqcommand)+","+str(biascommand)+","+str(ampcommand)
        lastsendtime=time()
    else:
        rospy.sleep(0.01)

    #rospy.sleep(0.1)
def joy_listener():
    rospy.init_node('servofish_joy',anonymous=True)
    lastsendtime = time()
    rospy.Subscriber('/joy',Joy,joycallback)
    rospy.spin()

if __name__ == '__main__':
    joy_listener()