import numpy as np
import cv2
from matplotlib import pyplot as plt
import os

from collections import namedtuple

Vector = namedtuple("Vector","x y z")

bgr2rgb = lambda im: cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
rgb2bgr = lambda im: cv2.cvtColor(im, cv2.COLOR_RGB2BGR)

hsv2bgr = lambda im: cv2.cvtColor(im, cv2.COLOR_HSV2BGR)
bgr2hsv = lambda im: cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

bgr2gray = lambda im: cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
gray2bgr = lambda im: cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)

rgb2gray = lambda im: cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
gray2rgb = lambda im: cv2.cvtColor(im, cv2.COLOR_GRAY2RGB)


rad2deg = 180.0/np.pi
deg2rad = np.pi/180.0


def printCameraParams(P1):
    """
    Given a projection matrix, break it down into its components.
    """
    k1, r1, t1, _, _, _, _ = cv2.decomposeProjectionMatrix(P1)
    t1 = t1 / t1[3]
    print('Intrinsic Matrix:')
    print(k1)
    print('Rotation Matrix:')
    print(r1)
    print('Translation Vector:')
    print(t1.round(4).ravel())
    

def videoWriter(inframes, fname='out.mp4', fps=30, fourcc = 'avc1'):
    frames = [x for x in inframes]
    shape = frames[0].shape
    
    frame_height, frame_width = shape[:2]
    
    # video writer doesn't like grayscale images, have
    # to convert to RGB
    if len(shape) == 2:
        grayscale = True
    else:
        grayscale = False
    
    # fourcc = 'avc1'
    # fourcc = 'mjpg'
    
    print('>> Saving {} {}x{} images using {}'.format(len(frames), shape[1], shape[0], fourcc))
    
    # create the video writer and write all frames to the file
    out = cv2.VideoWriter(
        fname,
        cv2.VideoWriter_fourcc(*fourcc), 
        fps, 
        (frame_width,frame_height))
    
    for frame in frames:
        # convert if necessary to RGB
        if grayscale:
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
        else:
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out.write(frame)
    
    out.release()
    print(f'>> wrote {os.path.getsize(fname)/1e6:.1f} MB to {fname}')
    
    
# https://wiki.nps.edu/display/RC/Local+Coordinate+Frames
# https://www.researchgate.net/publication
#        /224239584_Rectilinear_coordinate_frames_for_Deep_sea_navigation

# deg2rad = np.pi/180.0

def  mdeglat(lat):
    '''
    Provides meters-per-degree latitude at a given latitude
    
    Args:
      lat (deg): latitude
    Returns:
      float: meters-per-degree value
    '''
    latrad = lat*deg2rad

    dy = 111132.09 - 566.05 * np.cos(2.0*latrad) \
        + 1.20 * np.cos(4.0*latrad) - 0.002 * np.cos(6.0*latrad)
    return dy

def mdeglon(lat):
    '''
    Provides meters-per-degree longitude at a given latitude
    Args:
      lat (deg): latitude in decimal degrees
    Returns:
      float: meters per degree longitude
    '''
    latrad = lat*deg2rad
    
    dx = 111415.13 * np.cos(latrad) \
        - 94.55 * np.cos(3.0*latrad) + 0.12 * np.cos(5.0*latrad)
    return dx

def ll2xy(lat, lon, orglat, orglon):
    '''
    AlvinXY: Lat/Long to X/Y
    Converts Lat/Lon (WGS84) to Alvin XYs using a Mercator projection.
    Args:
      lat (deg): Latitude of location
      lon (deg): Longitude of location
      orglat (deg): Latitude of origin location
      orglon (deg): Longitude of origin location
    Returns:
      tuple: (x,y) where...
        x is Easting in m (Alvin local grid)
        y is Northing in m (Alvin local grid)
    '''
    x = (lon - orglon) * mdeglon(orglat);
    y = (lat - orglat) * mdeglat(orglat);
    return (x,y)

def xy2latlon(x, y, lat0, lon0):
    """
    
    """
    lon = x/mdeglon(lat0) + lon0
    lat = y/mdeglat(lat0) + lat0
    return lat, lon

def imshow(img, cmap=None):
    if cmap:
        plt.imshow(img, cmap=cmap)
    else:
        plt.imshow(img)
    plt.title(f"{img.shape}")
    plt.axis("off")
    
# def pil2opencv(imgs, hist_equ=False):
#     if hist_equ:
#         ret = [cv2.equalizeHist(np.array(x)) for x in imgs]
#     else:
#         ret = [np.array(x) for x in imgs]
#     return ret

def plotSensors(imu, oxts, timestamps, degrees=False):
    a = np.array([x.accels for x in imu])
    w = np.array([x.gyros for x in imu])
    ts = timestamps
    if degrees:
        euler = np.array([x.euler for x in imu]) * rad2deg
    else:
        euler = np.array([x.euler for x in imu])

    plt.figure(figsize=(15,7))

    plt.subplot(221)
    plt.plot(ts, a[:,0], label="x-accel")
    plt.plot(ts, a[:,1], label="y")
    plt.plot(ts, a[:,2], label="z")
    plt.grid(True)
    plt.legend()
    # plt.title("Accels [m/sec^2]");
    plt.ylabel("m/sec^2")
    # plt.xlabel("Time [sec]")

    plt.subplot(222)
    plt.plot(ts, w[:,0], label="x-gyro")
    plt.plot(ts, w[:,1], label="y")
    plt.plot(ts, w[:,2], label="z")
    plt.grid(True)
    plt.legend()
    # plt.title("Gyros [rad/sec]");
    plt.ylabel("rad/sec")
    # plt.xlabel("Time [sec]")

    plt.subplot(223)
    plt.plot(ts, euler[:,0], label="roll")
    plt.plot(ts, euler[:,1], label="pitch")
    plt.plot(ts, euler[:,2], label="yaw")
    # plt.title("Euler Angles [deg]")
    if degrees:
        plt.ylabel("Degrees")
    else:
        plt.ylabel("Radians")
    # plt.xlabel("Time [sec]")
    plt.legend()
    plt.grid(True);

    plt.subplot(224)
    # y = [x.packet.lat for x in oxts]
    # x = [x.packet.lon for x in oxts]
    truth = np.array([x.T_w_imu[:3,3] for x in oxts])
    x = truth[:,0]
    y = truth[:,1]
    plt.plot(x,y,label="Truth")
    plt.plot(x[0],y[0],"go", label="start")
    plt.plot(x[-1],y[-1],"ro", label="stop")
    plt.grid(True)
    plt.legend()
    plt.axis('equal')
    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    # plt.title("True Path")
    # plt.title(f'Lat Lon [{y[0]:.2f}, {x[0]:.2f}]');