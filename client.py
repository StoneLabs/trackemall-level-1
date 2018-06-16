#import os
import time
import numpy as np
import cv2
from freenect import sync_get_depth as get_depth, sync_get_video as get_video
from numpy import asarray
from PIL import Image as PImage

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

if __name__ == "__main__":

    ##########################
    # Setup Qt-Window

    pg.setConfigOptions(antialias=True)
    application = QtGui.QApplication([])

    window = pg.GraphicsWindow()
    window.resize(1000,600)
    window.setWindowTitle("Quality Software.to")
    container = pg.ImageItem()
    containerplot = window.addPlot()
    containerplot.addItem(container)

    ##########################
    # Choose input method
    # and write to inp_mode
    # 1 = kinect & 0 = webcam 

    print("")
    print("Choose image source:")
    print(" - [0] Webcam")
    print(" - [1] MS-Kinect")
    print("> ", end='', flush=True)
    inp_mode = int(input())

    print("")
    if inp_mode == 0:
        success = False
        while (not success):
            print("Enter webcam id (0=default): ", end='')
            id=input()

            cap = cv2.VideoCapture(int(id))
            if(cap.isOpened()):
                print("Device opened successfully")
                success = True
            else:
                print("Couldn't open device")
    elif inp_mode == 1:
        print("Connecting to Kinect...")
    else:
        exit(1)

    ##########################
    # Start infinite loop
    # and write to inp_mode
    # 1 = kinect & 0 = webcam 
    
    while True:
        print("Reading frame")
        frame = None
        r = True
        if inp_mode == 0:
            r, frame = cap.read()
        elif inp_mode == 1:
            global depth, rgb
            (depth,_), (rgb,_) = get_depth(), get_video()
            frame = np.array(rgb)
        else:
            exit(1)

        if r:
            # Send away

            # multi threading magic

            # receive results (not here but somewhere):
#            for cat, score, bounds in results:
#                x, y, w, h = bounds
#                cv2.rectangle(frame, (int(x-w/2),int(y-h/2)),(int(x+w/2),int(y+h/2)),(255,0,0))
#                cv2.putText(frame, str(cat.decode("utf-8")), (int(x), int(y)), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0))

            container.setImage(asarray(PImage.fromarray(frame).rotate(-90)))
            cv2.waitKey(1) # find better (non-cv) solution for qt refreshing EDIT: no time -> just keep it
