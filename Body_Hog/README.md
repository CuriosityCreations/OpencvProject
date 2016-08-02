#Body Hog Recognization

Default haar for body recogniztion is bad, and default HOG is better


###Function Used:
1. hog = cv2.HOGDescriptor()
2. hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector())
3. found,w=hog.detectMultiScale(img, winStride=(8,8), padding=(32,32), scale=1.05)


###Input:
1. Target picture


###Output:
1. Maked Picture
