# import the necessary packages
#import argparse
import cv2
 
# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
cropping = False
 
def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, cropping, ix,iy, image, clone

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        ix,iy = x,y
        cropping = True
    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping == True:
            image = clone.copy()
            cv2.rectangle(image,(ix,iy),(x,y),[255, 0, 0],2)
    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        refPt.append((x, y))
        cropping = False

        # draw a rectangle around the region of interest
        cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
        #cv2.imshow("image", image)
        #cv2.imwrite('roi.jpg', image)

# construct the argument parser and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True, help="Path to the image")
#args = vars(ap.parse_args())
 
# load the image, clone it, and setup the mouse callback function
camera = cv2.VideoCapture("inputcar.avi")
ok, image=camera.read()
#image=cv2.resize(image,(0,0),fx = 0.25, fy = 0.25)
#image = cv2.imread("body2.jpg")
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)
tracker = cv2.Tracker_create("KCF")
init_once = False

# keep looping until the 'q' key is pressed
while True:
	# display the image and wait for a keypress
	cv2.imshow("image", image)
	key = cv2.waitKey(1) & 0xFF
 
	# if the 'r' key is pressed, reset the cropping region
	if key == ord("r"):
		image = clone.copy()
 
	# if the 'c' key is pressed, break from the loop
	elif key == ord("c"):
		break
 
# if there are two reference points, then crop the region of interest
# from teh image and display it
if len(refPt) == 2:
        #cv2.destroyAllWindows()
        #roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
        #cv2.imshow("ROI", roi)
        #cv2.imwrite('ROI.jpg', roi)
   bbox = (refPt[0][0],refPt[0][1],refPt[1][0]-refPt[0][0],refPt[1][1]-refPt[0][1])
   while 1:
       ok, image=camera.read()
       #image=cv2.resi`ze(image,(0,0),fx = 0.25, fy = 0.25)
       if not ok:
           print ('no image read')
           break

       if not init_once:
           ok = tracker.init(image, bbox)
           init_once = True

       ok, newbox = tracker.update(image)
       print (ok, newbox)

       if ok:
           p1 = (int(newbox[0]), int(newbox[1]))
           p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
           cv2.rectangle(image, p1, p2, (200,0,0),3)

       cv2.imshow("image", image)
       k = cv2.waitKey(1) & 0xff
       if k == 27 : break # esc pressed

# close all open windows
cv2.destroyAllWindows()
