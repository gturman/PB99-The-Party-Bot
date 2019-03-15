#!/usr/bin/env python

#emotion node
#Subscribers: /body, /eyes

import random
import Image
import ImageDraw
import numpy
import time
from rgbmatrix import Adafruit_RGBmatrix
import rospy
from std_msgs.msg import String, Int16, Float32

matrix = Adafruit_RGBmatrix(32, 1)

class Emotion:

    def __init__(self):
        self.name = "emotion"

        self.run = True

        self.w = 25
        self.h = 25
        self.r = 200
        self.g = 200
        self.b = 20

        #self.frames = 0.33

        rospy.init_node('emotion', anonymous=True)
        rospy.Subscriber("/w", Int16, self.widthcallback)
        rospy.Subscriber("/h", Int16, self.heightcallback)
        rospy.Subscriber("/r", Int16, self.redcallback)
        rospy.Subscriber("/g", Int16, self.greencallback)
        rospy.Subscriber("/b", Int16, self.bluecallback)
        #rospy.Subscriber("/frames", Float32, self.framescallback)
        #rate = rospy.Rate(10)
        rospy.sleep(2)
        looprate = rospy.Rate(60)
        while not rospy.is_shutdown():
            self.run = True
            looprate.sleep()           

    def widthcallback(self,msg):
        self.w = msg.data
        self.displayemotion()
    def heightcallback(self,msg):
        self.h = msg.data
        self.displayemotion()
    def redcallback(self,msg):
        self.r = msg.data
        self.displayemotion()
    def greencallback(self,msg):
        self.g = msg.data
        self.displayemotion()
    def bluecallback(self,msg):
        self.b = msg.data
        self.displayemotion()
    #def framescallback(self,msg):
        #self.frames = msg.data
        #self.displayemotion()

    def displayemotion(self):
        red = self.r-50
        blue = self.g-50
        green = self.b-50
        image = Image.new("RGB",(32,32),(self.r-50,self.g-50,self.b-50))
        draw = ImageDraw.Draw(image)
        draw.ellipse((15-(self.w/2),15-(self.h/2),self.w,self.h),fill=(self.r+50,self.g+50,self.b+50),outline=(self.r,self.g,self.b))
        matrix.SetImage(image.im.id,0,0)	
        time.sleep(0.02)

if __name__ == "__main__":
    node = Emotion()
    rospy.spin()
