#C.T.Chen All Rights Reserved

import cv2
import numpy as np
import sys
import time



if __name__ == '__main__':

  #MQTT + GPIO
  GPIO = 1
  #dual camera
  camera1 = cv2.VideoCapture('inputcar.avi')
  camera2 = cv2.VideoCapture('inputcar.avi')
  hogfound = False
  init_once = False

  while(GPIO):
      #Depth Map
      okL, frameL = camera1.read()
      okR, frameR = camera2.read()
     
      if not (okL and okR):
          break
      _frameL = cv2.cvtColor(frameL, cv2.COLOR_BGR2GRAY)
      _frameR = cv2.cvtColor(frameR, cv2.COLOR_BGR2GRAY)

      active = False
      disparity = []
      if okL and okR:
          active = True
          stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
          disparity = stereo.compute(_frameL,_frameR)
          disparity = cv2.GaussianBlur(disparity, (5, 5), 0)
          #_disparity= cv2.cvtColor(disparity, cv2.COLOR_GRAY2BGR)

      found = []
      if not active:
          print("fail to initialize dual camera")
          break
      else:
          #HOG Locate
          hog = cv2.HOGDescriptor()
          hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
          found,w=hog.detectMultiScale(frameL, winStride=(8,8), padding=(32,32), scale=1.05)
          if (len(found) > 0):
              hogfound = True
              print(len(found))
              for (x,y,w,h) in found:
                  cv2.rectangle(frameL,(x,y),(x+w,y+h),(255,0,0),2)

      bbox = []
      if hogfound and not init_once:
          #Track the man in center
          for (x,y,w,h) in found:
              if x > camera1.get(3)/3 and x < camera1.get(3)* 2/3:
                  bbox = (x,y,w,h)
                  break
              else:
                  hogfound = False
      #KCF Tracking
      tracker = cv2.Tracker_create("KCF")
      if hogfound and not init_once:
          okT = tracker.init(disparity, bbox)
          init_once = True

      ok, newbox = tracker.update(disparity)
      if ok:
         p1 = (int(newbox[0]), int(newbox[1]))
         p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
         cv2.rectangle(disparity, p1, p2, (200,0,0),3)

      cv2.imshow('frame',disparity)
      #cv2.imshow('res',imgRes)
      k = cv2.waitKey(5) & 0xFF
      if k == 27:
          break
cv2.destroyAllWindows()     
    
    
    #Motor Conrol
