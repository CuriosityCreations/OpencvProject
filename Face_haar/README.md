#Face Haar Recognization

xml are default opencv traing results in /usr/local/share/OpenCV/haarcascades


###Function Used:
1. face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
2. faces = face_cascade.detectMultiScale(gray, 1.3, 5)


###Input:
1. Target picture


###Output:
1. Maked Picture
