import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)


import cv2
import numpy as np
import tensorflow as tf
from copy import deepcopy
sys.path.append("..")
import lib.label_map_util
import datetime
from tracker import *

'''
x1,y1 ------
|          |
|          |
|          |
--------x2,y2
'''

trackers_list = []
distance = 30
intensity = 10
allowed_classes = ['person', 'car', 'truck', 'bycicle', 'motorcycle', 'bus']


class Net:
    def __init__(self, graph_fp, labels_fp, num_classes=90, threshold=0.6):
        self.graph_fp = graph_fp
        self.labels_fp = labels_fp
        self.num_classes = num_classes

        self.graph = None
        self.label_map = None
        self.categories = None
        self.category_index = None

        self.bb = None
        self.bb_origin = None
        self.image_tensor = None
        self.boxes = None
        self.scores = None
        self.classes = None
        self.num_detections = None

        self.in_progress = False
        self.session = None
        self.threshold = threshold
        with tf.device('/gpu:0'):
            self._load_graph()
            self._load_labels()
            self._init_predictor()

    def _load_labels(self):
        self.label_map = lib.label_map_util.load_labelmap(self.labels_fp)
        self.categories = lib.label_map_util.convert_label_map_to_categories(self.label_map, max_num_classes=self.num_classes, use_display_name=True)
        self.category_index = lib.label_map_util.create_category_index(self.categories)

    def _load_graph(self):
        self.graph = tf.Graph()
        with self.graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.graph_fp, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
        tf.get_default_graph().finalize()

    def _display(self, direction, camera, zone, out, filtered_results, processed_img, display_img):
        
        global trackers_list
        try:
            localize(trackers_list)
        except Exception as e:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)    

        h, w, _ = processed_img.shape
        h_dis, w_dis, _ = display_img.shape
        ratio_h = float(h_dis) / h
        ratio_w = float(w_dis) / w

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        font_color = (0, 255, 0)
        line_type = 2
        offset = 20

        new_positions = []

        for res in filtered_results:
            if res["class"] in allowed_classes :
                y1, x1, y2, x2 = res["bb_o"]
                y1, y2 = int(y1 * ratio_h), int(y2 * ratio_h)
                x1, x2 = int(x1 * ratio_w), int(x2 * ratio_w)
                if out:
                    cv2.rectangle(display_img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                roi =  display_img[y1:y2, x1:x2]
                new_positions.append((((x1+x2)/2),((y1+y2)/2),intensity, roi))
                '''cv2.putText(display_img, res["class"],
                            (x1 + offset, y1 - offset),
                            font,
                            font_scale,
                            font_color,
                            line_type)'''

        try:
            trackers_list = updater(trackers_list, new_positions, distance)
        except Exception as e:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

        try:    
            trackers_list = cleaner(trackers_list)
        except Exception as e:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        
        try:    
            main_positions = track_main(trackers_list)
        except Exception as e:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

        
        if main_positions:
            for p in main_positions:
                try:
                    idd = 'ID :' + str(p[3])
                    if out:
                        cv2.putText(display_img, idd,
                            (int(p[0]), int(p[1]) - 45),
                            font,
                            font_scale,
                            font_color,
                            line_type)
                except Exception as e:
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        if out:
            if zone:
                cv2.line(display_img,(zone[0][0],zone[0][1]),(zone[1][0],zone[1][1]),(255,0,0),3)

        try:
            trajectory(direction, camera, trackers_list, display_img, zone, out)                
        except Exception as e:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

        if out:
            cv2.imshow('img', display_img)
            # cv2.waitKey()
            # cv2.destroyAllWindows()

    def _init_predictor(self):
        tf_config = tf.ConfigProto(device_count={'gpu': 0}, log_device_placement=True)
        tf_config.gpu_options.allow_growth = True
        with self.graph.as_default():
            self.session = tf.Session(config=tf_config, graph=self.graph)
            self.image_tensor = self.graph.get_tensor_by_name('image_tensor:0')
            self.boxes = self.graph.get_tensor_by_name('detection_boxes:0')
            self.scores = self.graph.get_tensor_by_name('detection_scores:0')
            self.classes = self.graph.get_tensor_by_name('detection_classes:0')
            self.num_detections = self.graph.get_tensor_by_name('num_detections:0')

    def predict(self, direction, camera, zone, out, img, display_img):
        self.in_progress = True
        start = datetime.datetime.now().microsecond * 0.001

        with self.graph.as_default():
            #print('[INFO] Read the image ..')

            img_copy = deepcopy(img)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            height, width, _ = img.shape
            #print('[INFO] Shape of this image is -- [heigh: %s, width: %s]' % (height, width))

            image_np_expanded = np.expand_dims(img, axis=0)

            #print('[INFO] Detecting objects ...')
            session_start = datetime.datetime.now().microsecond * 0.001
            (boxes, scores, classes, num_detections) = self.session.run(
                [self.boxes, self.scores, self.classes, self.num_detections],
                feed_dict={
                    self.image_tensor: image_np_expanded
                })
            session_end = datetime.datetime.now().microsecond * 0.001
            #print('[INFO] Filtering results ...')
            filtered_results = []			
            for i in range(0, len(scores[0])):
                score = scores[0][i]
                if score >= self.threshold:
                    y1, x1, y2, x2 = boxes[0][i]
                    y1_o = int(y1 * height)
                    x1_o = int(x1 * width)
                    y2_o = int(y2 * height)
                    x2_o = int(x2 * width)
                    predicted_class = self.category_index[classes[0][i]]['name']
                    filtered_results.append({
                        "score": score,
                        "bb": boxes[0][i],
                        "bb_o": [y1_o, x1_o, y2_o, x2_o],
                        "img_size": [height, width],
                        "class": predicted_class
                    })
                    #print('[INFO] %s: %s' % (predicted_class, score))

            # print 'Displaying %s objects against raw images ... ' % num_detections

            end = datetime.datetime.now().microsecond * 0.001
            elapse = end - start
            fps = np.round(1000.0 / elapse, 3)
            session_elapse = session_end - session_start
            sfps = np.round(1000.0 / session_elapse, 3)
            #print('+++++++++++++++++++++++ SFPS: ', sfps)
            #print('----------------------- FPS: ', fps)
            if fps > 0:
                cv2.putText(display_img, 'FPS: %s' % fps, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            self._display(direction, camera, zone, out, filtered_results, processed_img=img_copy, display_img=display_img)
        # session.close()
        # del session
        self.in_progress = False

    def get_status(self):
        return self.in_progress

    def kill_predictor(self):
        self.session.close()
        self.session = None
