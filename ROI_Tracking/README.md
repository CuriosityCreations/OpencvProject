# ROI Tracking

###Function:

```tracker = cv2.Tracker_create("MIL")``` (KCF, TLD)


```ok = tracker.init(image, bbox)```


```ok, newbox = tracker.update(image)```

###Input:
Image
Bouncing box

###Output
Booling OK or not
Bouncing box

# KCF method has bugs #640

https://github.com/opencv/opencv_contrib/issues/640

