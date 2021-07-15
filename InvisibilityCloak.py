import cv2
import numpy

#Trackbar callback function
def nothing(x):
	pass

#Initialise default camera 
cap = cv2.VideoCapture(0)
trackbars = cv2.namedWindow("Track bars")

cv2.createTrackbar("upper_hue","Track bars",110,180,nothing)
cv2.createTrackbar("upper_saturation","Track bars",255, 255, nothing)
cv2.createTrackbar("upper_value","Track bars",255, 255, nothing)
cv2.createTrackbar("lower_hue","Track bars",68,180, nothing)
cv2.createTrackbar("lower_saturation","Track bars",55, 255, nothing)
cv2.createTrackbar("lower_value","Track bars",54, 255, nothing)

#Capturing the original background frame
while(True):
	cv2.waitKey(1000)
	ret, initial_frame = cap.read()
	if(ret):
		break

#Capturing frames for invisiblility cloak
while(True):
	ret, frame = cap.read()
	converted_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	#getting the HSV values for masking cloak
	upper_hue = cv2.getTrackbarPos("upper_hue", "Track bars")
	upper_saturation = cv2.getTrackbarPos("upper_saturation", "Track bars")
	upper_value = cv2.getTrackbarPos("upper_value", "Track bars")
	lower_value = cv2.getTrackbarPos("lower_value","Track bars")
	lower_hue = cv2.getTrackbarPos("lower_hue","Track bars")
	lower_saturation = cv2.getTrackbarPos("lower_saturation","Track bars")

	#kernel used for dilation
	kernel = numpy.ones((3, 3), numpy.uint8)

	upper_hsv = numpy.array([upper_hue,upper_saturation,upper_value])
	lower_hsv = numpy.array([lower_hue,lower_saturation,lower_value])

	mask = cv2.inRange(converted_frame, lower_hsv, upper_hsv)
	mask = cv2.medianBlur(mask, 3)
	mask_inverse = 255 - mask
	mask = cv2.dilate(mask, kernel, 5)

	#Combining frames to achieve the desired frame
	b = frame[:,:,0]
	g = frame[:,:,1]
	r = frame[:,:,2]
	b = cv2.bitwise_and(mask_inverse, b)
	g = cv2.bitwise_and(mask_inverse, g)
	r = cv2.bitwise_and(mask_inverse, r)
	frame_inverse = cv2.merge((b, g, r))

	b = initial_frame[:,:,0]
	g = initial_frame[:,:,1]
	r = initial_frame[:,:,2]
	b = cv2.bitwise_and(mask, b)
	g = cv2.bitwise_and(mask, g)
	r = cv2.bitwise_and(mask, r)
	cloak_area = cv2.merge((b, g, r))

	final_frame = cv2.bitwise_or(frame_inverse, cloak_area)

	cv2.imshow("Invisibility Cloak", final_frame)

	if(cv2.waitKey(3) == ord('q')):
		break;

cv2.destroyAllWindows()
cap.release()
