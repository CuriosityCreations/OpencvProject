# -*- coding: utf-8 -*-
"""
Created on Sun May 10 11:17:13 2015

@author: José María Sola Durán
"""

import cv2
import os
import numpy as np
import utilscv

# It has created a Python class, called Image Feature
# containing for each of the images in the database,
# the information necessary to compute object recognition.
class ImageFeature(object):
    def __init__(self, nameFile, shape, imageBinary, kp, desc):
        #Filename
        self.nameFile = nameFile
        #Shape image
        self.shape = shape
        #binary image data
        self.imageBinary = imageBinary
        #Keypoints image after applying the detection algorithm features
        self.kp = kp
        #Descriptors of the features detected
        self.desc = desc
        #Matchings image database with the image of the webcam
        self.matchingWebcam = []
        #Matching Webcam with the current image of the database.
        self.matchingDatabase = []
    #For emptying the matching calculated previously for a new image
    def clearMatchingMutuos(self):
        self.matchingWebcam = []
        self.matchingDatabase = []

#Function responsible for calculating, for each of the methods of calculation features,
#the features of each of the images of the directory "models"
def loadModelsFromDirectory():
    #The Method returns a dictionary. The key is the algorithm features
    #mientras that the value is a list of objects of type ImageFeature
    #donde all data is stored on the features of the images of the
    #Database
    dataBase = dict([('SIFT', []), ('AKAZE', []), ('SURF', []), 
                     ('ORB', []), ('BRISK', [])])
    #It has limited the number of features 250, so that the fluid will algorithm.
    sift = cv2.xfeatures2d.SIFT_create(nfeatures=250)
    akaze = cv2.AKAZE_create()
    surf = cv2.xfeatures2d.SURF_create(800)
    orb = cv2.ORB_create(400)
    brisk = cv2.BRISK_create()
    for imageFile in os.listdir("modelos"):
        #the image is loaded with OpenCV
        colorImage = cv2.imread("modelos/" + str(imageFile))
        #We passed the image to grayscale
        currentImage = cv2.cvtColor(colorImage, cv2.COLOR_BGR2GRAY)
        #We conducted a resize image so that the image compared equal
        kp, desc = sift.detectAndCompute(currentImage, None)
        #print(desc)
        #print("xxxxxxxxxxxxxxxxx1111")
        #the features are loaded with SIFT
        dataBase["SIFT"].append(ImageFeature(imageFile, currentImage.shape, colorImage, kp, desc))
        #the features are loaded with AKAZE
        kp, desc = akaze.detectAndCompute(currentImage, None)
        #print(desc)
        #print("xxxxxxxxxxxxxxxxx2222")
        dataBase["AKAZE"].append(ImageFeature(imageFile, currentImage.shape, colorImage, kp, desc))
        #the features are loaded with SURF
        kp, desc = surf.detectAndCompute(currentImage, None)
        dataBase["SURF"].append(ImageFeature(imageFile, currentImage.shape, colorImage, kp, desc))
        #the features are loaded with ORB
        kp, desc = orb.detectAndCompute(currentImage, None)
        dataBase["ORB"].append(ImageFeature(imageFile, currentImage.shape, colorImage, kp, desc))
        #the features are loaded with BRISK
        kp, desc = brisk.detectAndCompute(currentImage, None)
        dataBase["BRISK"].append(ImageFeature(imageFile, currentImage.shape, colorImage, kp, desc))
    return dataBase
    
#Function responsible for calculating the mutual Matching, but nesting loops
#Is a very slow solution because no power is used Numpy
#Even put a slider to use this method because it is very slow

def findMatchingMutuos(selectedDataBase, desc, kp):
    for imgFeatures in selectedDataBase:
        imgFeatures.clearMatchingMutuos()
        for i in range(len(desc)):
            primerMatching = None
            canditatoDataBase = None
            matchingSegundo = None
            candidateWebCam = None
            
            for j in range(len(imgFeatures.desc)):
                valorMatching = np.linalg.norm(desc[i] - imgFeatures.desc[j])
                if (primerMatching is None or valorMatching < primerMatching):
                    primerMatching = valorMatching
                    canditatoDataBase = j
            for k in range(len(desc)):
                valorMatching = np.linalg.norm(imgFeatures.desc[canditatoDataBase] - desc[k])
                if (matchingSegundo is None or valorMatching < matchingSegundo):
                    matchingSegundo = valorMatching
                    candidateWebCam = k
            if not candidateWebCam is None and i == candidateWebCam:
                imgFeatures.matchingWebcam.append(kp[i].pt)
                imgFeatures.matchingDatabase.append(imgFeatures.kp[canditatoDataBase].pt)
    return selectedDataBase

#Function responsible for calculating the mutual matching of an image of the webcam,
#with all the images of the database. Receives as input
#the database depending on the method of calculation used features
#image input webcam.
def findMatchingMutuosOptimizado(selectedDataBase, desc, kp):
    #The algorithm is repeated for each image of the database.
    for img in selectedDataBase:
        img.clearMatchingMutuos()
        for i in range(len(desc)):
             #the norm of the difference of the current descriptor is calculated, with all
             #image descriptors of the database. We get
             #without loops and using the broadcasting of Numpy, all distances
             #between the current descriptor with all descriptors of the current image
             distanceListFromWebCam = np.linalg.norm(desc[i] - img.desc, axis=-1)
             #the candidate who is less distance from the current descriptor is obtained
             candidatoDataBase = distanceListFromWebCam.argmin()
             
             #print(distanceListFromWebCam)
             #print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxx000")
             #Checks whether the matching is mutual, ie, if met
             #in the other direction. That is, it is found that the candidatoDatabase
             #It has the current descriptor as best matching
             distanceListFromDataBase = np.linalg.norm(img.desc[candidatoDataBase] - desc,
                                           axis=-1)
             
             #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
             candidatoWebCam = distanceListFromDataBase.argmin()
             #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


             #print(candidatoWebCam)
             #print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxx111")
             #print(i)
             #print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxx222")
             #If mutual matching is met, it is stored for later treat
             if (i == candidatoWebCam):
                img.matchingWebcam.append(kp[i].pt)
                img.matchingDatabase.append(img.kp[candidatoDataBase].pt)
        #Por comodidad se convierten en Numpy ND-Array
        img.matchingWebcam = np.array(img.matchingWebcam)
        img.matchingDatabase = np.array(img.matchingDatabase)
        #print(img.matchingWebcam)
    return selectedDataBase

# This function calculates the best picture depending on the number of inliers
# That each image database of the image obtained
# The webcam.
def calculateBestImageByNumInliers(selectedDataBase, projer, minInliers):
    if minInliers < 15:
        minInliers = 15
    bestIndex = None
    bestMask = None
    numInliers = 0
    #To Each of the images
    for index, imgWithMatching in enumerate(selectedDataBase):
        #method 1,3,4 no data out
        #RANSAC algorithm is computed to calculate the number of inliers
        #print(len(imgWithMatching.matchingDatabase))
        if not len(imgWithMatching.matchingDatabase) is 0:
            _, mask = cv2.findHomography(imgWithMatching.matchingDatabase, 
                                     imgWithMatching.matchingWebcam, cv2.RANSAC, projer)
        if len(imgWithMatching.matchingDatabase) is 0:
            mask = None
        if not mask is None:
            #A Checks, from the number of inliers mask.
            #If the number of inliers is above the minimum number of inliers,
            #and is a maximum (inliers has more than the previous image) 
            #entonces is considered to be the image that fits with the object
            #almacenado in the database.
            countNonZero = np.count_nonzero(mask)
            if (countNonZero >= minInliers and countNonZero > numInliers):
                numInliers = countNonZero
                bestIndex = index
                bestMask = (mask >= 1).reshape(-1)
    #If an image is obtained as the best picture and therefore
    #debe have a minimum number of inlers, then you are finally calculas
    #The keypoints that are inliers from the mask obtained in findHomography
    #and is returned as best picture.
    if not bestIndex is None:
        bestImage = selectedDataBase[bestIndex]
        inliersWebCam = bestImage.matchingWebcam[bestMask]
        inliersDataBase = bestImage.matchingDatabase[bestMask]
        return bestImage, inliersWebCam, inliersDataBase
    return None, None, None
                
#This Function calculates the affinity matrix A, paints a rectangle around
#del detected object and paints in a new window image data base
#correspondiente the recognized object
def calculateAffinityMatrixAndDraw(bestImage, inliersDataBase, inliersWebCam, imgout):
    #A Calculates the affinity matrix A
    A = cv2.estimateRigidTransform(inliersDataBase, inliersWebCam, fullAffine=True)
    A = np.vstack((A, [0, 0, 1]))
    
    #A Calculated points of the rectangle that occupies the recognized object
    a = np.array([0, 0, 1], np.float)
    b = np.array([bestImage.shape[1], 0, 1], np.float)
    c = np.array([bestImage.shape[1], bestImage.shape[0], 1], np.float)
    d = np.array([0, bestImage.shape[0], 1], np.float)
    centro = np.array([float(bestImage.shape[0])/2, 
       float(bestImage.shape[1])/2, 1], np.float)
       
    #A Multiply the points of the virtual space, to become
    #puntos real image
    a = np.dot(A, a)
    b = np.dot(A, b)
    c = np.dot(A, c)
    d = np.dot(A, d)
    centro = np.dot(A, centro)
    
    #A Deshomogeneizan points
    areal = (int(a[0]/a[2]), int(a[1]/b[2]))
    breal = (int(b[0]/b[2]), int(b[1]/b[2]))
    creal = (int(c[0]/c[2]), int(c[1]/c[2]))
    dreal = (int(d[0]/d[2]), int(d[1]/d[2]))
    centroreal = (int(centro[0]/centro[2]), int(centro[1]/centro[2]))
    
    #A Paints the polygon and the file name of the image in the center of the polygon
    points = np.array([areal, breal, creal, dreal], np.int32)
    cv2.polylines(imgout, np.int32([points]),1, (255,255,255), thickness=2)
    utilscv.draw_str(imgout, centroreal, bestImage.nameFile.upper())
    #A Displays the detected object in a window part
    cv2.imshow('ImageDetector', bestImage.imageBinary)
