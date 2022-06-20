#!/usr/bin/env python3
# https://docs.opencv.org/3.4.3/d5/dae/tutorial_aruco_detection.html
# https://docs.opencv.org/3.4.3/df/d4a/tutorial_charuco_detection.html
# https://github.com/opencv/opencv_contrib/issues/1845
# https://github.com/opencv/opencv_contrib/issues/1698

# simple marker detection
import numpy as np
import cv2
import cv2.aruco as aruco

image = cv2.imread("2.png")
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_250)
# parameters = aruco.DetectorParameters_create()
corners, ids, rejectedImgPoints = aruco.detectMarkers(image, aruco_dict)
# ret, corners, ids = aruco.interpolateCornersCharuco(corners, ids, image, board)
# print(corners, ids, rejectedImgPoints)
aruco.drawDetectedMarkers(image, corners, ids)
# aruco.drawDetectedMarkers(image, rejectedImgPoints, borderColor=(100, 0, 240))

print(">> Press any key to exit\n")
cv2.imshow('so52814747', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
