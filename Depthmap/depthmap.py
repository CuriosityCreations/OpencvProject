import cv2
import numpy as np

imgL = cv2.imread('left.png', 0)
imgR = cv2.imread('right.png', 0)

stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
disparity = stereo.compute(imgL,imgR)

cv2.imwrite('disparity.png',disparity)

blur = cv2.GaussianBlur(disparity, (5, 5), 0)

cv2.imwrite('blur.png',blur)

