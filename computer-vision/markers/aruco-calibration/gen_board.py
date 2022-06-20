#!/usr/bin/env python3
import cv2
from cv2 import aruco
import argparse


def run(x, y, sqr, mark, dictionary, dpi, fname):
    board = aruco.CharucoBoard_create(x,y,sqr,mark,dictionary)

    sz = (x*dpi, y*dpi)
    boarderbits = 1
    img = board.draw(sz, None, 0, boarderbits)

    cv2.imshow('marker', img)
    print("Menu")
    print("  [s]ave the board to {}".format(fname))
    print("  Any key to exit")
    key = cv2.waitKey()

    if key == ord('s'):
        print(">> saved ...")
        cv2.imwrite(fname, img)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
    Creates a CharucoBoard
    square block size > marker size
    """)
    parser.add_argument("-x", help="number of horizontal blocks, default: 5", type=int, default=5)
    parser.add_argument("-y", help="number of vertical blocks, default: 7", type=int, default=7)
    parser.add_argument("--filename", "-f", help="file name, default: board.png", default='board.png')
    parser.add_argument("--marker_size", "-m", help="edge length of marker blocks, default: 0.75", type=float, default=0.75)
    parser.add_argument("--square_size", "-s", help="edge length of square blocks, default: 1.0", type=float, default=1.0)
    parser.add_argument("--dict", "-d", help="dictionary, default: aruco.DICT_4X4_50", default=aruco.DICT_4X4_50)
    parser.add_argument("--dpi", help="dots per inch, default: 100", type=int, default=100)
    args = parser.parse_args()

    run(
        args.x,
        args.y,
        args.square_size,
        args.marker_size,
        aruco.Dictionary_get(args.dict),
        args.dpi,
        args.filename
    )
