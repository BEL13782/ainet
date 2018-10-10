from models import object_detection
from models.zoning import *
from config import config
import cv2
import sys
import tensorflow as tf
import numpy as np
from loader import load_cameras




model_name = config.models["1"]
net = object_detection.Net(graph_fp='%s/frozen_inference_graph.pb' % model_name,
                           labels_fp='data/label.pbtxt',
                           num_classes=90,
                           threshold=0.6)
CAMERA_MODE = 'camera'
STATIC_MODE = 'static'
IMAGE_SIZE = 320



def demo(mode=CAMERA_MODE):
    cameras = load_cameras()
    camera = cameras[0]
    if mode == STATIC_MODE:
        try:
            if 'ab-easy' in camera['ip']:
                cap = cv2.VideoCapture('videos/ab-easy2.mp4')
            else:    
                cap = cv2.VideoCapture(camera['ip'])
            ret, frame = cap.read()
        
            
            #line = None
            while (cap.isOpened()):
                ret, frame = cap.read()
                net.predict(camera['direction'], camera['id'], camera['line'], False, img=frame, display_img=frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        except Exception as e:
            print(str(e))
    elif mode == CAMERA_MODE:
        cap = cv2.VideoCapture(0)

        while True:
            with tf.device('/gpu:0'):
                ret, frame = cap.read()
                in_progress = net.get_status()
                if ret and (not in_progress):
                    resize_frame = cv2.resize(frame, (IMAGE_SIZE, IMAGE_SIZE))
                    net.predict(img=resize_frame, display_img=frame)
                else:
                    print('[Warning] drop frame or in progress')
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    demo(mode=STATIC_MODE)