#!/usr/bin/env python

import cv2
import time

if __name__ == '__main__' :
    # read from default camera - 0
    # video = cv2.VideoCapture(0)
    # read from a movie, mp4
    video = cv2.VideoCapture("Megamind.mp4")

    while True:
        ok, frame = video.read()
        if ok:
            cv2.imshow('movie', frame)
            k = cv2.waitKey(1)
            if k == ord('q'):
                exit()
            time.sleep(0.033)

        else:
            break
