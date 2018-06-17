#import os
import time
import numpy as np
import cv2
from freenect import sync_get_depth as get_depth, sync_get_video as get_video
from numpy import asarray
from PIL import Image as PImage

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

import pickle
import subprocess

target_fps = 15
seconds_buffer = 10
ms_sleep = 1/target_fps

if __name__ == "__main__":

    ##########################
    # Setup Qt-Window

    pg.setConfigOptions(antialias=True)
    application = QtGui.QApplication([])

    window = pg.GraphicsWindow()
    window.resize(1000,600)
    window.setWindowTitle("Quality Software.to detection visualizer")
    container = pg.ImageItem()
    containerplot = window.addPlot()
    containerplot.addItem(container)

    ##########################
    # Start infinite loop
    # and write to inp_mode
    # 1 = kinect & 0 = webcam 
    
    time_outcounter = 0
    frame_counter = -(seconds_buffer * target_fps)
    while True:
        time_start = time.time()
        window.setWindowTitle("Quality Software.to detection visualizer FRAME " + str(frame_counter))
        cv2.waitKey(1) # find better (non-cv) solution for qt refreshing EDIT: no time -> just keep it

        if frame_counter > 0:
            try:
                # unpickle results and frame
                print("Grabbing frame #" + str(frame_counter) + "\t", end='', flush=True)
                cmd = ['wget', "127.0.0.1:2438/getDetection?id=" + str(frame_counter), "-O", "/tmp/tta.frame." + str(frame_counter), "wb+"]
                prc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, input="")


                print("\rGrabbing frame #" + str(frame_counter) + " [  LOADING  ]\t", end='', flush=True)
                with open("/tmp/tta.frame." + str(frame_counter), "rb") as handle:
                    dataframe = pickle.load(handle)

                frame = dataframe["frame"]
                results = dataframe["results"]

                print("\rGrabbing frame #" + str(frame_counter) + " [ RENDERING ]\t", end='', flush=True)
                # receive results (not here but somewhere):
                for cat, score, bounds in results:
                    x, y, w, h = bounds
                    cv2.rectangle(frame, (int(x-w/2),int(y-h/2)),(int(x+w/2),int(y+h/2)),(255,0,0))
                    cv2.putText(frame, str(cat.decode("utf-8")), (int(x), int(y)), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0))
                container.setImage(asarray(PImage.fromarray(frame).rotate(-90)))
                cv2.waitKey(1) # find better (non-cv) solution for qt refreshing EDIT: no time -> just keep it
            except:
                pass

        time_end = time.time()
        time_sleep = ms_sleep - (time_end - time_start)
        if time_sleep < 0:
            time_outcounter += 1
            if time_outcounter > 5:
                print("System cant keep up.")
                exit(1)
        else:
            time_outcounter = 0
            time.sleep(time_sleep)
        frame_counter += 1
