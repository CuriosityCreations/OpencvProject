import numpy as np
import cv2

hog = cv2.HOGDescriptor()

hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
img = cv2.imread('people.jpg')
found,w=hog.detectMultiScale(img, winStride=(8,8), padding=(32,32), scale=1.05)

for (x,y,w,h) in found:
  cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
  #roi_gray = gray[y:y+h, x:x+w]
  #roi_color = img[y:y+h, x:x+w]
  #eyes = eye_cascade.detectMultiScale(roi_gray)
  #for (ex,ey,ew,eh) in eyes:
    #cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)


cv2.imwrite('people.png', img)
