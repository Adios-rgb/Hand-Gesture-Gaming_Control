import cv2
import numpy as np
import time, imutils
import math
import pydirectinput


time_for_camera_warmup = 3
min_contour_area = 2000
cap = cv2.VideoCapture(0)
time.sleep(time_for_camera_warmup)

try:
    while True:
        counter = 0
        try:
            _, frame = cap.read()
			# ROI where hand needs to be placed and image processing will be performed
            roi = frame[50:300, 100:350]
            cv2.rectangle(frame, (100,50), (350,300), (128,128,128), 1)
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

            '''lower and upper bound HSV to mask the hand only. The values
            might change depending on your background or lighting conditions.
            Feel free to experiment with these values'''            
            lower_bound = np.array([0, 80, 60])
            upper_bound = np.array([25, 255, 255])
            mask = cv2.inRange(hsv, lower_bound, upper_bound)
            kernel = np.ones((3,3), dtype=np.uint8)
            
            # Image processing to clean noisy pixels
            dil = cv2.dilate(mask, kernel, iterations=4)
            mask = cv2.GaussianBlur(dil, (3,3), 100)
            opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
            cv2.imshow('closing', closing)
            
            cnts = cv2.findContours(closing, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            if len(cnts) > 0:
                max_area_cnt = max(cnts, key = cv2.contourArea)
                # Min contour area set so that contour is not formed on any background objects
                if cv2.contourArea(max_area_cnt) > min_contour_area:
                    x, y, w, h = cv2.boundingRect(max_area_cnt)
                    cv2.drawContours(roi, [max_area_cnt], -1, (0,0,255), 3)
                    # Convex hull is the smallest convex polygon that connects and encloses all points of a contour
                    hull = cv2.convexHull(max_area_cnt)
                    cv2.drawContours(roi, [hull], -1, (0,255,0), 2)
                    # To find the convexity defects in the hull. Defect is an area that do not belong to the object but located inside of its outer boundary
                    hull2 = cv2.convexHull(max_area_cnt, returnPoints=False)
                    defects = cv2.convexityDefects(max_area_cnt, hull2)
                    # Inside the loop coordinates of start, end and far points are computed which will be the three points of a triangle
                    for i in range(defects.shape[0]):
                        s, e, f, d = defects[i, 0]
                        start = tuple(max_area_cnt[s][0])
                        end = tuple(max_area_cnt[e][0])
                        far = tuple(max_area_cnt[f][0])
                        
                        a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                        b = math.sqrt((start[0] - far[0]) ** 2 + (start[1] - far[1]) ** 2)
                        c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                        s = a + b + c / 2
                        # Area of the triangle
                        ar = math.sqrt(s * (s - a) * (s - b) * (s - c))
                        d = ar * 2 / a
                        angle = math.acos((b ** 2 + c ** 2 - a ** 2)/(2 * b * c)) * 57
                        # Condition to eliminate defects which are not forming between fingers
                        if angle <= 90 and d > 30:
                            counter += 1
                            cv2.circle(roi, far, 5, (255,0,0), -1)
                    '''One added to counter as defects will be one less than fingers shown, i.e if five fingers shown then,
                    defects ideally should be four and four plus one is five'''
                    counter += 1
                    if counter == 5:
                        cv2.putText(frame, str(counter), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,0,0), 2)
                        pydirectinput.keyDown('left')
                    elif counter == 4:
                        cv2.putText(frame, str(counter), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,0,0), 2)
                    elif counter == 3:
                        cv2.putText(frame, str(counter), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,0,0), 2)
                    elif counter == 2:
                        cv2.putText(frame, str(counter), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,0,0), 2)
                    elif counter == 1:
                        cv2.putText(frame, str(counter), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,0,0), 2)
                        pydirectinput.keyDown('right')
                cv2.imshow('frame', frame)
            else:
                pydirectinput.keyUp('left')
                pydirectinput.keyUp('right')
            if cv2.waitKey(1) & 0xff == 27:
                break
        except Exception as e:
            print(str(e))
            continue
except Exception as e:
    print(str(e))

cap.release()
cv2.destroyAllWindows()