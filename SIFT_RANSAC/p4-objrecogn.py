#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python required module
import sys
import cv2
import time

# python required utility
import utilscv
import objrecogn as orec

# main function:
if __name__ == '__main__':

    # Creating window and associated sliders and mouse callback:
    # Trackbar onChange: do nothing
    def nothing(*arg):
        pass

    cv2.namedWindow('Features')
    cv2.namedWindow('ImageDetector')

    #Selecting the method for computing features
    #1, 3, 4 fail now
    cv2.createTrackbar('method', 'Features', 0, 4, nothing)
    #Playback error to calculate inliers with RANSAC
    cv2.createTrackbar('projer', 'Features', 5, 10, nothing)
    #Inliers minimum number to indicate that it has recognized an object
    cv2.createTrackbar('inliers', 'Features', 20, 50, nothing)
    #Trackbar to indicate whether the features are painted or not
    cv2.createTrackbar('drawKP', 'Features', 0, 1, nothing)

    # Opening video source
    if len(sys.argv) > 1:
        strsource = sys.argv[1]
    else:
        strsource = '0:400:300'  # Simple opening of the zero camera without scaling

    splitstr = strsource.split(':')
    Videonum, Width, Height = [int(i) for i in splitstr]
    cap = cv2.VideoCapture('inputcar.avi')

    paused = False
    methodstr = 'None'

    #We load the database models
    dataBaseDictionary = orec.loadModelsFromDirectory()
    
    while True:
        # Reading input frame and interface parameters:
        if not paused:
            ret, frame = cap.read()
            frame = cv2.resize(frame, (Width, Height))
        if frame is None:
            print('End of video input')
            break

        # Creating detector features, according to method (only at first):
        method = cv2.getTrackbarPos('method', 'Features')
        if method == 0:
            if methodstr != 'SIFT':
                methodstr = 'SIFT'
                detector = cv2.xfeatures2d.SIFT_create(nfeatures=250)
        elif method == 1:
            if methodstr != 'AKAZE':
                methodstr = 'AKAZE'
                detector = cv2.AKAZE_create()
        elif method == 2:
            if methodstr != 'SURF':
                methodstr = 'SURF'
                detector = cv2.xfeatures2d.SURF_create(800)
        elif method == 3:
            if methodstr != 'ORB':
                methodstr = 'ORB'
                detector = cv2.ORB_create(400)
        elif method == 4:
            if methodstr != 'BRISK':
                detector = cv2.BRISK_create()
                methodstr = 'BRISK'
                
        # We spent input image to gray:
        imgin = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # It is estimated the output image
        imgout = frame.copy()
        # We detect features, and measure time:
        t1 = time.time()
        kp, desc = detector.detectAndCompute(imgin, None)
        #print(desc)
        selectedDataBase = dataBaseDictionary[methodstr]
        if len(selectedDataBase) > 0:
            #We realize mutual matching
            imgsMatchingMutuos = orec.findMatchingMutuosOptimizado(selectedDataBase, desc, kp)    
            minInliers = int(cv2.getTrackbarPos('inliers', 'Features'))
            projer = float(cv2.getTrackbarPos('projer', 'Features'))
            #the best image is calculated based on the number of inliers. 
            #The best image is one that has more number of inliers, but always
            #exceeding the minimum indicated in the trackbar 'mini pliers'
            bestImage, inliersWebCam, inliersDataBase =  orec.calculateBestImageByNumInliers(selectedDataBase, projer, minInliers)            
            if not bestImage is None:
                #If we find a good image, the affinity matrix is calculated and the recognized object is painted on the screen.
               orec.calculateAffinityMatrixAndDraw(bestImage, inliersDataBase, inliersWebCam, imgout)
               
        t1 = 1000 * (time.time() - t1)  # Time in milliseconds
        # Get dimension of descriptors for each feature:
        if desc is not None:
            if len(desc) > 0:
                dim = len(desc[0])
            else:
                dim = -1
        # Features draw and write text about the image
        # Only features are drawn if the slider indicates
        if (int(cv2.getTrackbarPos('drawKP', 'Features')) > 0):
            cv2.drawKeypoints(imgout, kp, imgout,
                              flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        utilscv.draw_str(imgout, (20, 20),
                         "Method {0}, {1} features found, desc. dim. = {2} ".
                         format(methodstr, len(kp), dim))
        utilscv.draw_str(imgout, (20, 40), "Time (ms): {0}".format(str(t1)))
        # Show results and check keys:
        cv2.imshow('Features', imgout)
        ch = cv2.waitKey(5) & 0xFF
        if ch == 27:  # escape ends
            break
        elif ch == ord(' '):  # Spacebar pause
            paused = not paused
        elif ch == ord('.'):  # Point moves forward one frame
            paused = True
            ret, frame = cap.read()

    # Close windows and fonts video:
    cap.release()
    cv2.destroyAllWindows()
