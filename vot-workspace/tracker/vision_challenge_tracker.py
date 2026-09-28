#!/usr/bin/python

import vot
import sys
import time
import cv2
import numpy
import collections

class VCTracker(object):

    def __init__(self, image, region):
        self.window = max(region.width, region.height) * 2

        left = max(region.x, 0)
        top = max(region.y, 0)

        right = min(region.x + region.width, image.shape[1] - 1)
        bottom = min(region.y + region.height, image.shape[0] - 1)

        #Initial template
        self.template = image[int(top):int(bottom), int(left):int(right)]
        #self.template = cv2.cvtColor(self.template,cv2.COLOR_BGR2GRAY)
        #Center position of the template (u,v)
        self.position = (region.x + region.width / 2, region.y + region.height / 2)
        #Size of the template (width, height)
        self.size = (region.width, region.height)
        
        #im = cv2.rectangle(image, (int(left), int(top)), (int(right), int(bottom)), (255,0,0), 2)
        #cv2.imshow('result',im)
        #cv2.imshow('template',self.template)
        #cv2.waitKey(0) #change 0 to 1 - remove waiting for key press


    def track(self, image):

        margen = 26
        #left = 0
        #top = 0
        confidence = 0

        centroX, centroY = self.position
        zonaLeft = max(0, int(centroX - self.size[0] / 2 - margen))
        zonaTop = max(0, int(centroY - self.size[1] / 2 - margen))
        zonaRight = min(image.shape[1], int(centroX + self.size[0] / 2 + margen))
        zonaBottom = min(image.shape[0], int(centroY + self.size[1] / 2 + margen))

        imgRecortada = image[zonaTop:zonaBottom, zonaLeft:zonaRight]

        result = cv2.matchTemplate(imgRecortada, self.template, cv2.TM_SQDIFF_NORMED)
        #result = cv2.matchTemplate(imgRecortada, self.template, cv2.TM_CCOEFF_NORMED)

        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)

        leftOriginal = zonaLeft + minLoc[0]
        topOriginal = zonaTop + minLoc[1]
        
        confidence = 1.0 - minVal

        """

        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
        leftOriginal = zonaLeft + maxLoc[0]
        topOriginal = zonaTop + maxLoc[1]

        confidence = maxVal

        """

        self.position = (leftOriginal + self.size[0] / 2, topOriginal + self.size[1] / 2)

	
        return vot.Rectangle(leftOriginal, topOriginal, self.size[0], self.size[1]), confidence
        
        
# *****************************************
# VOT: Create VOT handle at the beginning
#      Then get the initializaton region
#      and the first image
# *****************************************
handle = vot.VOT("rectangle")
selection = handle.region()

# Process the first frame
imagefile = handle.frame()
if not imagefile:
    sys.exit(0)
image = cv2.imread(imagefile)

# Initialize the tracker
tracker = VCTracker(image, selection)

while True:
    # *****************************************
    # VOT: Call frame method to get path of the
    #      current image frame. If the result is
    #      null, the sequence is over.
    # *****************************************
    imagefile = handle.frame()
    if not imagefile:
        break
    image = cv2.imread(imagefile)
    
    # Track the object in the image  
    region, confidence = tracker.track(image)
    
    #Use these lines for testing.
    # Comment them when you evaluate with the vot toolkit
    im = cv2.rectangle(image,(int(region.x),int(region.y)),(int(region.x+region.width),int(region.y+region.height)), (255,0,0), 2)
    cv2.imshow('result',im)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
    
    # *****************************************
    # VOT: Report the position of the object
    #      every frame using report method.
    # *****************************************
    handle.report(region, confidence)

