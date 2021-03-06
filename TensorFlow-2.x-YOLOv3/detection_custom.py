#Script adapted from:
#================================================================
#
#   File name   : detection_custom.py
#   Author      : PyLessons
#   Created date: 2020-09-17
#   Website     : https://pylessons.com/
#   GitHub      : https://github.com/pythonlessons/TensorFlow-2.x-YOLOv3
#   Description : object detection image and video example
#
#================================================================

import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
import cv2
import numpy as np
import tensorflow as tf
from yolov3.utils import detect_image, detect_video, Load_Yolo_model
from yolov3.configs import *

def detectInput(fname, save, showConfidence, violationOnly):
    splitedFname = fname.split(".")

    if ((splitedFname[-1] == "jpg") | (splitedFname[-1] == "jpeg")):
        yolo = Load_Yolo_model()
        return(detect_image(yolo, fname, save, input_size=YOLO_INPUT_SIZE, show=False, CLASSES=TRAIN_CLASSES, rectangle_colors=(255,0,0), showConfidence=showConfidence, violationOnly=violationOnly))
    else:
        yolo = Load_Yolo_model()
        detect_video(yolo, fname, save, input_size=YOLO_INPUT_SIZE, show=True, CLASSES=TRAIN_CLASSES, rectangle_colors=(255,0,0), showConfidence=showConfidence, violationOnly=violationOnly) #BGR
