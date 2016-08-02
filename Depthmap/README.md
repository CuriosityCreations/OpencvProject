#Depth Map Example

###Function used:

1. ```img = cv2.GaussianBlur(disparity, (7,7), 0)``` (img, mask(odd, odd), deviation in x)
2. ```img = cv2.StereoBM_create(numDisparities=16, blockSize=15)``` (search range, block size)

###Input:
1. left.png
2. right.png

###Output:
1. disparity.png (depth map)
2. blur.png (Gaussian blurred map)

