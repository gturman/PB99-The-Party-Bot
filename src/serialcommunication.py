#!/usr/bin/env python

#serial communication node
#Subscribers: /status
#Publishers: /body

import serial
import sys
import argparse
import time
import rospy
from std_msgs.msg import String

class SerialCommunication:
    def __init__(self):
        self.name="serialcommunication"
        self.run = True

        #self.port = rospy.get_param('~port')
        #self.baudrate = rospy.get_param('~baudrate')
        self.port = '/dev/ttyACM0'
        self.baudrate = 115200
        self.ser = serial.Serial(self.port, self.baudrate)
        self.ser.writeTimeout = 0

        rospy.init_node('serialcommunication', anonymous=True)
        rospy.Subscriber("/status", String, self.statuscallback)

        self.status= ""
        self.body = ""
        #struct
        #CENTER_SONAR
        #LEFT_IR
        #RIGHT_IR
        #ACCEL
        #GYRO
        #BEHAVIOR
        self.need2write = False
        
        while(self.run):
            self.run = True
            if self.need2write: self.write2serial()

    def statuscallback(self,msg):
        #print "statuscallback received: " + msg.data + "\n"
        self.status = msg.data
        self.need2write = True

    def write2serial(self):
        if self.status != None:
            self.ser.flushOutput()
            self.ser.write(self.status.encode())
            rospy.sleep(1.5)
            print "!!!Writing to serial: " + str(self.status) + "\n"
            self.need2write = False
            self.ser.flushOutput()

    #def publishbody(self):
        #self.bodypub.publish(self.body)

    def getbodyinfo(self):
        if (self.ser.inWaiting() > 3):
             inByte = self.ser.readline()
             #print str(inByte) + "\n"

if __name__ == "__main__":
    node = SerialCommunication()
    rospy.spin()
    #while(node.run):
        #node.write2serial()
