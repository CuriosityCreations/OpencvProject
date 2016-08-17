import numpy as np
import cv2
import glob

# Input Image from pic/ 
# Find Pedestrian ROI and save to hogresult/
# Calculate the hitrate
# Ptype = "jpg", "bmp", ....
def Hogdetect(Hit,Pic,Ptype):
  for imgfile1 in glob.glob("pic/*."+ Ptype):
    Pic +=1
    img = cv2.imread(imgfile1)

    found,w=hog.detectMultiScale(img, winStride=(8,8), padding=(32,32), scale=1.05)
  
    if (len(found) > 0):
      Hit +=1
      for (x,y,w,h) in found:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

      filename = imgfile1.split("pic/")[1]
      cv2.imwrite("hogresult/" + filename.split("."+ Ptype)[0] + "_HOG." + Ptype, img)
  return Hit, Pic


if __name__ == '__main__':

  hog = cv2.HOGDescriptor()
  hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

  Hit, Pic = 0, 0
  Hit, Pic = Hogdetect(Hit,Pic,"jpg")
  Hit, Pic = Hogdetect(Hit,Pic,"bmp")

  hitrate = Hit / Pic
  print("Hitrate = %.2f"% hitrate )
