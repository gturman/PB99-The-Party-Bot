#!/usr/bin/env python

#behavior node
#Subscribers: /body, /eyes
#Publishers: /status, /rgb, /wh, /frames

import random
import numpy
import time
import rospy
from std_msgs.msg import String, Int16, Float32

WAIT_DURATION = 60
ROAM_DURATION = 2

class Behavior:

    def __init__(self):
        self.name = "behavior"

        self.run = True

        #self.body = ""
        self.eyes = "NUL"
        self.status = "wait"

        self.bloodalcoholcontent = 0

        self.width = 24
        self.height = 24
        self.red = 200
        self.green = 200
        self.blue = 10
        #self.framerate = 0.33

        self.starttime = 0

        self.waiting = True
        self.roaming = False

        rospy.init_node('behavior', anonymous=True)

        self.status_pub = rospy.Publisher('/status', String, queue_size=1)

        self.width_pub = rospy.Publisher('/w', Int16, queue_size=1)
        self.height_pub = rospy.Publisher('/h', Int16, queue_size=1)

        self.red_pub = rospy.Publisher('/r', Int16, queue_size=1)
        self.green_pub = rospy.Publisher('/g', Int16, queue_size=1)
        self.blue_pub = rospy.Publisher('/b', Int16, queue_size=1)

        #self.framerate_pub = rospy.Publisher('/f', Float32, queue_size=1)

        #rospy.Subscriber("/body", String, bodycallback)
        rospy.Subscriber("/eyes", String, self.eyescallback)
        #rate = rospy.Rate(10)

        rospy.sleep(5)
        self.publishemotion(29,29,20,20,20)
        rospy.sleep(6)
        print "content mode...\n"
        print "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB\n"
        self.publishemotion(26,26,20,20,200)
        self.publishstatus("content")
        rospy.sleep(2.8)
        print "excited mode...\n"
        print "RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR\n"
        self.publishemotion(30,30,200,20,20)
        self.publishstatus("excited")
        rospy.sleep(6.8)
        print "gross mode...\n"
        print "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG\n"
        self.publishemotion(24,24,20,200,20)
        self.publishstatus("gross")
        rospy.sleep(3.2)
        print "start!\n"
        self.publishemotion(25,25,20,20,20)
        self.publishstatus(self.status)
        rospy.sleep(3)

        self.starttime = rospy.get_time()
        
        #looprate = rospy.Rate(0.001)
        while (True):
            self.havefeelings()
            rospy.sleep(0.2)
            #print "currently " + self.status + "\n\n\nxxxxx"
            #rospy.spin()

    #def bodycallback(self,msg):
        #self.body = msg

    def eyescallback(self,msg):
        if self.waiting:
            print "IN CALL BACK!!!!!!!!!!!!!!!!!!!\n"
            self.eyes = msg.data
            self.whatbeeristhis()#updates status if beer found
        else: 
            print "not looking ------- \n"
        #print "subscriber heard: " + str(self.eyes) + "\n"

    def publishstatus(self,s):
        self.status_pub.publish(s)
        rospy.sleep(1)
        #self.status_pub.publish(s)
        #print "publishing status: " + str(s) + "\n"
        #rospy.sleep(1)
    
    def publishemotion2(self,w,h,r,g,b):
        print w + h + r + g + b


    def publishemotion(self,w,h,r,g,b):
        self.width_pub.publish(w)
        self.height_pub.publish(h)
        self.red_pub.publish(r)
        self.green_pub.publish(g)
        self.blue_pub.publish(b)
        #rospy.sleep(1)
        #self.framerate_pub.publish(f)
        #print "publishing emotion: " + str(w) + ","+ str(h) + ","+ str(r) + ","+ str(g) + ","+ str(b) + ","+ str(f) + "\n"

    def whatbeeristhis(self):
        
        if self.eyes == "sho":
            #self.publishstatus("excited")
            #rospy.sleep(6)
            self.status = "excited"
        elif self.eyes == "lag":
            #self.publishstatus("gross")
            #rospy.sleep(3)
            self.status = "gross"
        elif self.eyes == "blu":
            #self.publishstatus("content")
            #rospy.sleep(3)
            self.status = "content"
        else: 
            self.width = 26
            self.height = 26
            self.red = 20
            self.green = 200
            self.blue = 250
            print "SHOULDNT BE HERE!!!!!!!!!!!!!!!!!!\n"

        if self.eyes != "NUL":
            self.bloodalcoholcontent = self.bloodalcoholcontent + 1
        if self.bloodalcoholcontent > 21:
            self.drunk = True
            print "DRUNK MODE ACTIVATED ALERT!!!!!!!!!!!!!!!! \n"

        print "analysis saw: " + str(self.eyes) + "\n"
    
    def havefeelings2(self):
        self.status="excited"
        self.publishstatus(self.status)
        rospy.sleep(10)
        self.status="content"
        self.publishstatus("content")
        rospy.sleep(10)

    def havefeelings(self):
        if self.waiting:
             #print "waitin\n"
             self.width = random.randrange(24,30,1)
             self.height = random.randrange(24,30,1)
             self.red = random.randrange(220,240,1)
             self.green = random.randrange(220,240,1)
             self.blue = random.randrange(10,20,1)
        elif self.roaming:
             #print "roamin\n"
             self.width = random.randrange(22,28,1)
             self.height = random.randrange(22,28,1)
             self.red = random.randrange(240,260,1)
             self.green = random.randrange(140,160,1)
             self.blue = random.randrange(10,20,1) 
            #if self.waiting: self.status = "wait"
            #elif self.roaming: self.status = "roam"
            #self.publishstatus(self.status)
        self.publishemotion(self.width,self.height,self.red,self.green,self.blue)
        
        #print "IN MAIN!!!!!!!!!!!!!!!!!!!! \n"
        endtime = rospy.get_time()
        elapsed = endtime - self.starttime
        #print "start time:   " + str(self.starttime)
        #print "current time: " + str(endtime)
        #print "elapsed time: " + str(elapsed)
        if self.waiting == True:
            #self.publishstatus("wait")
            #print "WAITING\n"
            if elapsed > WAIT_DURATION:
                print "publish roam, wait duration over, waited: " + str(elapsed) + "\n"
                self.starttime = rospy.get_time()
                self.status = "roam"
                self.publishstatus("roam")
                rospy.sleep(1)
                self.waiting = False
                self.roaming = True
        elif self.roaming == True:
            #self.publishstatus("roam")
            #print "ROAMING\n"
            if elapsed > ROAM_DURATION:
                print "publish wait, roam duration over, roamed: " + str(elapsed) + "\n"
                self.starttime = rospy.get_time()
                self.status = "wait"
                self.publishstatus("wait")
                rospy.sleep(1)
                self.waiting = True
                self.roaming = False
        else:
            print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
                    
        if self.status == "excited":
            self.publishemotion(30,30,200,20,20)
            self.publishstatus("excited")
            print "RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR\n"
            print "---------sleeping for excited... \n"
            rospy.sleep(6.8)
            if self.waiting: self.status = "wait"
            elif self.roaming: self.status = "roam"
            print "returning to status " + str(self.status) + "\n"
            self.publishemotion(25,25,20,20,20)
            self.publishstatus(self.status)
            rospy.sleep(1)
        elif self.status == "gross":
            self.publishemotion(24,24,20,200,20)
            self.publishstatus("gross")
            print "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG\n"
            print "---------sleeping for gross... \n"
            rospy.sleep(3.2)
            if self.waiting: self.status = "wait"
            elif self.roaming: self.status = "roam"
            print "returning to status " + str(self.status) + "\n"
            self.publishemotion(25,25,20,20,20)
            self.publishstatus(self.status)
            rospy.sleep(1)
        elif self.status == "content":
            self.publishemotion(26,26,20,20,200)
            self.publishstatus("content")
            print "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB\n"
            print "--------sleeping for content.. \n"
            rospy.sleep(2.8)
            if self.waiting: self.status = "wait"
            elif self.roaming: self.status = "roam"
            print "returning to status " + str(self.status) + "\n"
            self.publishemotion(25,25,20,20,20)
            self.publishstatus(self.status)
            rospy.sleep(1)
        

        #if self.status == "wait" and self.waiting != True:
        #self.publishstatus(self.status)
        #rospy.sleep(0.1)

if __name__ == "__main__":
    node = Behavior()
    rospy.spin()
