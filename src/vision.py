#!/usr/bin/env python
'''
    def takealook(self):
        ret, self.raw_image = self.camera.read()


        for index in range(len(flannmatches)):
            masks[index] = [[0,0] for i in xrange(len(flannmatches[index]))]
            for i,(m,n) in enumerate(flannmatches[index]):
                if m.distance < flanncheck*n.distance:
                    masks[index][i]=[1,0]
            draw_params[index]= dict(matchColor = (0,255,0),singlePointColor = (255,0,0),matchesMask = masks[index],flags = 0)

''' 
#vision node
#Subscribers: None
#Publishers: /eyes

import picamera
import picamera.array
import time
import cv2
import rospy
from std_msgs.msg import String
import numpy
import io
import imutils

HESSIAN_THRESHOLD = 300#200
FRAME_RESIZE_FACTOR = 2#3
TEMPLATE_RESIZE_FACTOR = 1#2
FLANN_DISTANCE_SENS = 0.75#0.75
FLANN_MATCH_COUNT_SENS = 20 #11
COMPARE_SENS = 9#9

class Vision:
    
    def __init__(self):
        self.name = "vision"

        self.run = True
        self.isee = "NUL"

        self.camera = picamera.PiCamera()
        self.camera.resolution = (640,480)
        self.camera.framerate = 32
        #camera_port = 0
        #self.camera = cv2.VideoCapture(camera_port)
        self.raw_image = None
        self.image_analysis = None
        self.display_last_match = None

        #keypoints and descriptors, data 
        self.bl_kp = None
        self.pbr_kp = None
        self.yl_kp = None
        self.gu_kp = None
        self.sn_kp = None
        self.lg_kp = None
        self.st_kp = None
        self.bm_kp = None
        self.bl_des = None
        self.pbr_des = None
        self.yl_des = None 
        self.gu_des = None 
        self.sn_des = None
        self.lg_des = None
        self.st_des = None
        self.bm_des = None
        

        rospy.init_node('vision', anonymous=True)
        self.vision_pub = rospy.Publisher('/eyes', String, queue_size=1)
        #rate = rospy.Rate(10)

        #surf initialization
        self.surf = cv2.xfeatures2d.SURF_create(HESSIAN_THRESHOLD)
        #flann matcher initializations
        FLANN_INDEX_KDTREE=0
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        #self.flann = cv2.FlannBasedMatcher(index_params,search_params)
        #bruteforce
        self.bruteforce = cv2.BFMatcher()

        self.learnaboutbeer()
        print "init vision node\n"
        rospy.sleep(2)

        while (self.run):
            self.analysis()
            #self.showwhatisee()

    def takealook(self):
        #get data as RGB array from camera
        rawCapture = picamera.array.PiRGBArray(self.camera)        
        self.camera.capture(rawCapture, format="bgr", use_video_port=True)
        #store data as numpy array for OpenCV
        self.raw_image = rawCapture.array

        #clear camera data array
        rawCapture.truncate()


    def learnaboutbeer(self):

        #budlight = cv2.imread('/home/pi/partystack/src/partybot/src/beer/budlight.jpg',cv2.IMREAD_GRAYSCALE)
        #pbr = cv2.imread('/home/pi/partystack/src/partybot/src/beer/pbr.png',cv2.IMREAD_GRAYSCALE)
        #yuengling = cv2.imread('/home/pi/partystack/src/partybot/src/beer/yuengling.png',cv2.IMREAD_GRAYSCALE)
        #guinness = cv2.imread('/home/pi/partystack/src/partybot/src/beer/guinness.png',cv2.IMREAD_GRAYSCALE)
        #sierranevada = cv2.imread('/home/pi/partystack/src/partybot/src/beer/sierranevada.png',cv2.IMREAD_GRAYSCALE)
        lagunitas = cv2.imread('/home/pi/partystack/src/partybot/src/beer/lagunitas.png',cv2.IMREAD_GRAYSCALE)
        shocktop = cv2.imread('/home/pi/partystack/src/partybot/src/beer/shocktop.png',cv2.IMREAD_GRAYSCALE)
        bluemoon = cv2.imread('/home/pi/partystack/src/partybot/src/beer/bluemoon.png',cv2.IMREAD_GRAYSCALE)

        #budlight = imutils.resize(budlight, width=250/TEMPLATE_RESIZE_FACTOR)
        #pbr = imutils.resize(pbr, width=250/TEMPLATE_RESIZE_FACTOR)
        #yuengling = imutils.resize(yuengling, width=250/TEMPLATE_RESIZE_FACTOR)
        #guinness = imutils.resize(guinness, width=250/TEMPLATE_RESIZE_FACTOR)
        #sierranevada = imutils.resize(sierranevada, width=250/TEMPLATE_RESIZE_FACTOR)
        lagunitas = imutils.resize(lagunitas, width=250/TEMPLATE_RESIZE_FACTOR)
        shocktop = imutils.resize(shocktop, width=250/TEMPLATE_RESIZE_FACTOR)
        bluemoon = imutils.resize(bluemoon, width=250/TEMPLATE_RESIZE_FACTOR)

        #self.bl_kp, self.bl_des = self.surf.detectAndCompute(budlight,None)
        #self.pbr_kp, self.pbr_des = self.surf.detectAndCompute(pbr,None)
        #self.yl_kp, self.yl_des = self.surf.detectAndCompute(yuengling,None)
        #self.gu_kp, self.gu_des = self.surf.detectAndCompute(guinness,None)
        #self.sn_kp, self.sn_des = self.surf.detectAndCompute(sierranevada,None)
        self.lg_kp, self.lg_des = self.surf.detectAndCompute(lagunitas,None)
        self.st_kp, self.st_des = self.surf.detectAndCompute(shocktop,None)
        self.bm_kp, self.bm_des = self.surf.detectAndCompute(bluemoon,None)

        print "learned all beer\n"

    def analysis(self):

        self.takealook()

        #get frame from webcam, grayscale and resize
        grayframe = None
        grayframe = cv2.cvtColor(self.raw_image, cv2.COLOR_BGR2GRAY)
        h,w= grayframe.shape
        grayframe = imutils.resize(grayframe, width=w/FRAME_RESIZE_FACTOR)
        #init surf and surf the current frame
        keypoints, descriptors = self.surf.detectAndCompute(grayframe,None)
        #self.image_analysis = cv2.drawKeypoints(grayframe,keypoints,None,(0,0,255),4)

        #find matches between current frame and beer in database
        #match_frameVSbl= self.bruteforce.knnMatch(self.bl_des,descriptors,k=2)
        #match_frameVSpbr= self.bruteforce.knnMatch(self.pbr_des,descriptors,k=2)
        #match_frameVSyl= self.bruteforce.knnMatch(self.yl_des,descriptors,k=2)
        #match_frameVSgu= self.bruteforce.knnMatch(self.gu_des,descriptors,k=2)
        #match_frameVSsn= self.bruteforce.knnMatch(self.sn_des,descriptors,k=2)
        match_frameVSlg= self.bruteforce.knnMatch(self.lg_des,descriptors,k=2)
        match_frameVSst= self.bruteforce.knnMatch(self.st_des,descriptors,k=2)
        match_frameVSbm= self.bruteforce.knnMatch(self.bm_des,descriptors,k=2)

        #init lists to hold "good matches" produced by the flann matcher
        #good_bl = []
        #good_pbr = []
        #good_yl = []
        #good_gu = []
        #good_sn = []
        good_lg = []
        good_st = []
        good_bm = []
        #store "good matches"
        #if len(match_frameVSbl) > 0:
            #for m,n in match_frameVSbl:
                #if m.distance < FLANN_DISTANCE_SENS*n.distance:
                    #good_bl.append(m)
        #if len(match_frameVSpbr) > 0:
            #for m,n in match_frameVSpbr:
                #if m.distance < FLANN_DISTANCE_SENS*n.distance:
                    #good_pbr.append(m)
        #if len(match_frameVSyl) > 0:
            #for m,n in match_frameVSyl:
                #if m.distance < FLANN_DISTANCE_SENS*n.distance:
                    #good_yl.append(m)
        #if len(match_frameVSgu) > 0:
            #for m,n in match_frameVSgu:
                #if m.distance < FLANN_DISTANCE_SENS*n.distance:
                    #good_gu.append(m)
        #if len(match_frameVSsn) > 0:
            #for m,n in match_frameVSsn:
                #if m.distance < FLANN_DISTANCE_SENS*n.distance:
                    #good_sn.append(m)
        if len(match_frameVSlg) > 0:
            for m,n in match_frameVSlg:
                if m.distance < FLANN_DISTANCE_SENS*n.distance:
                    good_lg.append(m)
        if len(match_frameVSst) > 0:
            for m,n in match_frameVSst:
                if m.distance < FLANN_DISTANCE_SENS*n.distance:
                    good_st.append(m)
        if len(match_frameVSbm) > 0:
            for m,n in match_frameVSbm:
                if m.distance < FLANN_DISTANCE_SENS*n.distance:
                    good_bm.append(m)
        #print "good matches stored\n"
        #time.sleep(0.5)
        #make a list to hold each list of matches
        thinkaboutit = [0,0]
        #thinkaboutit = [len(good_bl),len(good_pbr),len(good_yl),len(good_gu),len(good_sn),len(good_lg),len(good_st),len(good_bm)]
        thinkaboutit = [len(good_lg),len(good_st),len(good_bm)]

	#print "goodbl len: " + str(len(good_bl)) + "\n"
        #print "goodpbr len: " + str(len(good_pbr)) + "\n"
	#print "goodyl len: " + str(len(good_yl)) + "\n"
        #print "goodgu len: " + str(len(good_gu)) + "\n"
	#print "goodsn len: " + str(len(good_sn)) + "\n"
        print "goodlg len: " + str(len(good_lg)) + "\n"
	print "goodst len: " + str(len(good_st)) + "\n"
        print "goodbm len: " + str(len(good_bm)) + "\n"
	print "max(thinkaboutit): " + str(max(thinkaboutit)) + "\n"
        #time.sleep(0.5)

        #if the max value of the list passes, then we can decide what beer we saw
        if max(thinkaboutit)>=FLANN_MATCH_COUNT_SENS:
            #print "checking against max list\n"
            #if len(good_bl) == max(thinkaboutit):
                #self.isee = "bud"
                #self.display_last_match = cv2.drawMatchesKnn(budlight,self.bl_kp,grayframe,keypoints,match_frameVSbl,None,**draw_params[0])
            #elif len(good_pbr) == max(thinkaboutit):
                #self.isee = "pbr"
            #elif len(good_yl) == max(thinkaboutit):
                #self.isee = "yue"
            #elif len(good_gu) == max(thinkaboutit):
                #self.isee = "gui"
            #elif len(good_sn) == max(thinkaboutit):
                #self.isee = "sie"
         
            if len(good_lg) == max(thinkaboutit):
                if (len(good_lg) > 23) and (len(good_st) < COMPARE_SENS) and (len(good_bm) < COMPARE_SENS):
                    self.isee = "lag"
                    self.publishwhatisee()
            elif len(good_st) == max(thinkaboutit):
                if (len(good_bm) < COMPARE_SENS) and (len(good_lg) < COMPARE_SENS):
                    self.isee = "sho"
                    self.publishwhatisee()
            elif len(good_bm) == max(thinkaboutit):
                if (len(good_lg) < COMPARE_SENS) and (len(good_st) < COMPARE_SENS):
                    self.isee = "blu"
                    self.publishwhatisee()
            else:
                self.isee = "NUL"
        #otherwise we saw nothing
        else: 
            self.isee = "NUL"

        #self.publishwhatisee()
        #self.showwhatisee()

        del grayframe
	#time.sleep(0.5)

    def publishwhatisee(self):
        self.vision_pub.publish(self.isee)
        print "from vision SAW SOMETHING and published: " + self.isee + "\n"
        rospy.sleep(3)

    def showwhatisee(self):
        cv2.imshow("Raw image", self.raw_image)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            exit()

    def showanalysis(self):
        cv2.imshow("SURF applied to raw image", self.image_analysis)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            exit()

    def showmatch(self):
        cv2.imshow("Last match", self.display_last_match)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            exit()


if __name__ == "__main__":
    node = Vision()
    rospy.spin()
