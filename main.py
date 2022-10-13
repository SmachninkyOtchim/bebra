import cv2
import numpy as np

ball_color = 'green'

color_dist = {'red': {'Lower': np.array([0, 60, 60]), 'Upper': np.array([0, 102, 255])},
             'blue': {'Lower': np.array([5, 160, 180]), 'Upper': np.array([124, 255, 255])},
             'green': {'Lower': np.array([35, 43, 35]), 'Upper': np.array([90, 255, 255])},
              }

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, flame = cap.read()
    if ret:
        if flame is not None:
            gs_flame = cv2.GaussianBlur(flame, (5, 5), 0)
            hsv = cv2.cvtColor(gs_flame, cv2.COLOR_BGR2HSV)
            erode_hsv = cv2.erode(hsv, None, iterations=2)
            inRange_hsv = cv2.inRange(erode_hsv, color_dist[ball_color]['Lower'], color_dist[ball_color]['Upper'])
            cnts = cv2.findContours(inRange_hsv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

            c = max(cnts, key=cv2.contourArea)
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            cv2.drawContours(flame, [np.int0(box)], -1, (0, 255, 255), 2)

            cv2.imshow('camera', flame)
            #cv2.imshow('Gauss', gs_flame)
            #cv2.imshow('HSV', hsv)
            #cv2.imshow('Erode', erode_hsv)
            #cv2.imshow()
            cv2.waitKey(1)
        else:
            print("Нет картинки")
    else:
        print("Невозможно прочитать камеру")

cap.release()
cv2.waitKey(0)
cv2.destroyAllWidows()
