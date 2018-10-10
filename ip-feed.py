import cv2
import requests
import numpy as np
from models import object_detection
from models.zoning import *
from config import config
import sys
import tensorflow as tf


model_name = config.models["1"]
net = object_detection.Net(graph_fp='%s/frozen_inference_graph.pb' % model_name,
                           labels_fp='data/label.pbtxt',
                           num_classes=90,
                           threshold=0.6)
CAMERA_MODE = 'camera'
STATIC_MODE = 'static'
IMAGE_SIZE = 320

working_cams = ["https://videos3.earthcam.com/fecnetwork/9974.flv/chunklist_w103796882.m3u8",
"http://192.65.213.243/mjpg/video.mjpg?COUNTER",
 "http://camera1.mairie-brest.fr/mjpg/video.mjpg?resolution=480x360",
 "http://166.165.35.32/mjpg/video.mjpg?COUNTER"]

#MANDATORY WARMUP !!!!!!!!!!!!!!!!!!!!!!!!!!
img_fp = 'test_images/1.jpg'
img = cv2.imread(img_fp)
net.predict(None, img=img, display_img=img)


r = requests.get(working_cams[0], stream=True)
if(r.status_code == 200):
    bytes = bytes()
    try:
        for chunk in r.iter_content(chunk_size=1024):
            bytes += chunk
            a = bytes.find(b'\xff\xd8')
            b = bytes.find(b'\xff\xd9')
            if a != -1 and b != -1:
                jpg = bytes[a:b+2]
                bytes = bytes[b+2:]
                i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                try:
                    net.predict(None, img=i, display_img=i)
                except Exception as e:
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                '''cv2.imshow('i', i)
                if cv2.waitKey(1) == 27:
                    exit(0)'''
    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)                
else:
    print("Received unexpected status code {}".format(r.status_code))