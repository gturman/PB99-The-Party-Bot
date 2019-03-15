#!/usr/bin/env python

import random
import Image
import ImageDraw
import numpy
import time
from rgbmatrix import Adafruit_RGBmatrix

matrix = Adafruit_RGBmatrix(32, 1)

matrix.Clear()	
time.sleep(0.5)
matrix.Fill(0xFF0000)
time.sleep(2)
matrix.Fill(0x00FF00)
time.sleep(2)
matrix.Fill(0x0000FF)
time.sleep(2)
matrix.Clear()

exit()
