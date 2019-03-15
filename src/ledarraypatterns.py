#!/usr/bin/env python

import random
import Image
import ImageDraw
import numpy
import time
from rgbmatrix import Adafruit_RGBmatrix

matrix = Adafruit_RGBmatrix(32, 1)

#16-(width/2),16-(height/2),width,height
emotion = 0x00FF00

while(True):
	#matrix.Clear()
	
	width = random.randrange(28,31,1)
	height = random.randrange(28,31,1)
	r =random.randrange(20,236,1) 
	g =random.randrange(20,30,1)
	b =random.randrange(20,30,1)

	image = Image.new("RGB",(32,32),(r-50,g-50,b-50))
	draw = ImageDraw.Draw(image)

	draw.ellipse((15-(width/2),15-(height/2),width,height),fill=(r+50,g+50,b+50),outline=(r,g,b))
	matrix.SetImage(image.im.id,0,0)	
	time.sleep(0.33)

exit()
