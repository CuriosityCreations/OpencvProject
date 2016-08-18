#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Utilidades varias para usar con OpenCV
'''

import cv2


# Auxiliary function to draw text contrast in an image:
def draw_str(dst, vec, s):
    cv2.putText(dst, s, (vec[0]+1, vec[1]+1), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 0),
                thickness=2, lineType=cv2.LINE_AA)
    cv2.putText(dst, s, vec, cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255),
                lineType=cv2.LINE_AA)


# Auxiliary function to cut an ROI on a given image size:
def fixroi(roi, imshape):
    if roi == ((-1, -1), (-1, -1)):
        rroi = ((0, 0), (imshape[1], imshape[0]))
    else:
        rroi = ((max(0, min(roi[0][0], roi[1][0])),
                 max(0, min(roi[0][1], roi[1][1]))),
                (min(imshape[1], max(roi[0][0], roi[1][0])),
                 min(imshape[0], max(roi[0][1], roi[1][1]))))
    return rroi


# Get the subimage given by a ROI:
def subimg(pimg, proi):
    return pimg[proi[0][1]:proi[1][1], proi[0][0]:proi[1][0]]


# Write the sub-picture given by a ROI:
def setsubimg(img1, img2, proi):
    img1[proi[0][1]:proi[1][1], proi[0][0]:proi[1][0]] = img2
