#C.T.Chen All Rights Reserved

import cv2
import numpy as np
import sys
import time

camera = cv2.VideoCapture("inputcar.avi")


if __name__ == '__main__':
    #MQTT Connect
    #Color Tracking
    while 1:
        ok, frame = camera.read()
        if not ok:
            break
        #cimg = frame[20:100, 40:100]

        imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        #blur image
        imgHSV = cv2.blur(imgHSV,(10,10))
        #imgHSV = cv2.GaussianBlur(imgHSV,(5,5),15,15)
        #imgHSV = cv2.medianBlur(imgHSV,5)

        # define range of blue color in HSV
        lower_blue = np.array([0,130,130])
        upper_blue = np.array([5,255,255])

        # Threshold the HSV image to get only red colors
        Colormask = cv2.inRange(imgHSV, lower_blue, upper_blue)

        # Bitwise-AND mask and original image
        imgRes = cv2.bitwise_and(frame,frame, mask=Colormask)

        # Covert to 1 channel image for contours
        imgRes = cv2.cvtColor(imgRes, cv2.COLOR_BGR2GRAY)

        #thresh = cv2.threshold(imgRes, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(imgRes, None, iterations=10)
        #thresh = cv2.erode(imgRes, None, iterations=1)
        im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        number = 0;
        for cnt in contours:
          x,y,w,h = cv2.boundingRect(cnt)
          cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
          area = cv2.contourArea(cnt)
          print("area = %4d, number = %d"%(area,number))
          number+=1
       
        cv2.imshow('frame',frame)
        #cv2.imshow('res',imgRes)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()
    #KCF
    #Motor Conrol
