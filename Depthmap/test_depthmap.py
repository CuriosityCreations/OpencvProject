import cv2
import numpy as np
import time

while 1:
  start = time.time()
  imgL = cv2.imread('left.png', 0)
  imgR = cv2.imread('right.png', 0)
  imgL = cv2.resize(imgL, (768,576))
  imgR = cv2.resize(imgR, (768,576))
  
  stereo = cv2.StereoBM_create(numDisparities=32, blockSize=31)
  disparity = stereo.compute(imgL,imgR)

  #cv2.imwrite('disparity.png',disparity)
  #blur = cv2.blur(disparity,(10,10))
  #blur = cv2.GaussianBlur(disparity, (5, 5), 0)
  blur = disparity

  #int16
  #print(blur.dtype)


  blur = cv2.normalize(blur, blur, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
  thresh = cv2.dilate(blur, None, iterations=1)
  #im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

  #cv2.imwrite('blur.png',blur)
  
  #number = 0;
  #for cnt in contours:
      #x,y,w,h = cv2.boundingRect(cnt)
      #cv2.rectangle(imgL,(x,y),(x+w,y+h),(0,255,0),2)
      #area = cv2.contourArea(cnt)
      #print("area = %4d, number = %d"%(area,number))
      #number+=1
  cv2.imshow('aa',thresh)
  k = cv2.waitKey(5) & 0xFF
  end = time.time()
  print("time = %.5f"%(end -start))
time.sleep(10)

