#!/usr/bin/env python

#ffmpeg -i vtest.avi -c:a aac -b:a 128k -c:v libx264 -crf 23 output.mp4

import numpy as np
import cv2

cap = cv2.VideoCapture('vtest.mp4')
# cap = cv2.VideoCapture(0)


def MOG(cap):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    print('kernel', kernel)
    # fgbg = cv2.createBackgroundSubtractorMOG()  # seems to be missing
    fgbg = cv2.createBackgroundSubtractorMOG2()
    # fgbg.setDetectShadows(False)

    frame_save = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # find the change
        fgmask = fgbg.apply(frame)
        # clean up the image
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

        frame_save += 1
        if 100 < frame_save <105:
            cv2.imwrite('frame{}.png'.format(frame_save), frame)

        cv2.imshow('frame',fgmask)
        k = cv2.waitKey(10)
        if k == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


def Subtract(cap):
    ret = False

    while not ret:
        ret, last = cap.read()
    last = cv2.cvtColor(last, cv2.COLOR_BGR2GRAY)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # smallest = np.amin(frame)
        # biggest = np.amax(frame)
        # print('max/min: {} {}'.format(smallest, biggest))


        change = frame - last
        last = frame
        # change = cv2.adaptiveThreshold(
        #     change,
        #     255,
        #     cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        #     cv2.THRESH_BINARY,
        #     11,2)
        # ret,change = cv2.threshold(change,200,255,cv2.THRESH_BINARY)

        cv2.imshow('frame',change)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

# Subtract(cap)
MOG(cap)
