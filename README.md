# Hand-Gesture-Gaming_Control
Extending finger counter for lateral movement gaming control.

**Functionality**

• Uses image processing techniques like masking, blur, contour detection, convex hull to find the outline of the palm and fingers from the Region of interest box.

• Counts the number of convexity defects from the convex hull to detect number of fingers.

• Press left key if finger count is 5 and move right if finger count is 1.

![image](https://user-images.githubusercontent.com/59373491/120937633-31a02780-c72c-11eb-9921-2f3a169b1716.png)

**Packages used**

• OpenCV

• Numpy

• imutils

• time

• pydirectinput

• math

**Steps involved for detecting fingers**

1.	Create a ROI box where user places his hand.
2.	Convert the images from BGR colorspace to HSV and apply masking
3.	Apply image processing techniques dilate, opening, closing etc. to remove noise.
4.	Find contours from the processed image and find contour with maximum area.
5.	Draw convex hull, find convexity defects.
6.	Loop over the defects and calculate the angle and length of one side of triangle.
7.	Draw the circle between the defects.
8.	Count of fingers will be one more than the count of defects.
9.	If count is 5 then press right and if count is 1 then press left.
