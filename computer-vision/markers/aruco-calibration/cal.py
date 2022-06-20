#!/usr/bin/env python3

import numpy as np
import cv2
import cv2.aruco as aruco
from glob import glob
import pickle

"""
Kevin.Walchko@DFEC-4508ZK aruco $ ./cal.py
Found 10 images at cal-imgs/*.png
0.4061621603751767
[[830.53534937   0.         338.16694656]
 [  0.         829.38390322 244.86232235]
 [  0.           0.           1.        ]]
[[-3.87605555e-02  8.70213792e-01  2.57513084e-04  1.08850726e-02
  -4.55056694e+00]]
"""

def get_images(path, gray=False):
    """
    Given a path, it reads all images. This uses glob to grab file names
    and excepts wild cards *
    Ex. cal.getImages('./images/*.jpg')
    """
    imgs = []
    files = glob(path)
    files.sort()

    print("Found {} images at {}".format(len(tuple(files)), path))
    # print('-'*40)

    for i, f in enumerate(files):
        img = cv2.imread(f)
        if img is None:
            print('>> Could not read: {}'.format(f))
        else:
            h, w = img.shape[:2]

            if gray:
                if len(img.shape) > 2:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            imgs.append(img)
    # print('-'*40)
    return imgs

def getPose(im, board, m, d):
    if len(im.shape) > 2:
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    else:
        gray = im
    # parameters = aruco.DetectorParameters_create()
    # corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, dictionary, parameters=parameters)
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, dictionary)
    ret, chcorners, chids = aruco.interpolateCornersCharuco(corners, ids, gray, board)
    ret, rvecs, tvecs = aruco.estimatePoseCharucoBoard(chcorners, chids, board,m,d)
    im = aruco.drawAxis(im, m, d, rvecs, tvecs,0.5)
    cv2.imshow('markers', im)
    cv2.waitKey()


dictionary = aruco.Dictionary_get(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters_create()
x = 8  # horizontal
y = 11  # vertical
sqr = 0.1  # solid black squares
mrk = 0.05 # markers, must be smaller than squares
board = aruco.CharucoBoard_create(x,y,sqr,mrk,dictionary)

imgs = get_images("cal-imgs/*.png", gray=False)

calcorners = []
calids = []

for im in imgs:
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    # corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, dictionary, parameters=parameters)
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, dictionary)
    # print('ids 1:', len(ids))
    # if ids were found, then
    if len(ids) > 0:
        # print(corners, ids, rejectedImgPoints)
        ret, chcorners, chids = aruco.interpolateCornersCharuco(corners, ids, gray, board)
        calcorners.append(chcorners)
        calids.append(chids)

        im2 = im.copy()
        aruco.drawDetectedCornersCharuco(im2, chcorners, chids)
        # aruco.drawDetectedMarkers(im2, rejectedImgPoints, borderColor=(100, 0, 240))

        cv2.imshow('markers', im2)
        cv2.waitKey()

ret, cameraMatrix, distCoeffs, rvecs, tvecs = aruco.calibrateCameraCharuco(calcorners, calids, board, gray.shape[::-1], None, None)
print('rms', ret)
print(cameraMatrix)
print(distCoeffs)

cam_params = {
    'marker_type': 'aruco',
    'cameraMatrix': cameraMatrix,
    'distCoeffs': distCoeffs,
    'image_size': imgs[0].shape[:2],
    'marker_size': (x,y),
    'marker_scale:': sqr
}
# im = cv2.cvtColor(imgs[0], cv2.COLOR_GRAY2BGR)
# print(im.shape)
getPose(imgs[9], board, cameraMatrix, distCoeffs)

cv2.destroyAllWindows()
