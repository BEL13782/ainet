import argparse
from pymongo import MongoClient
import datetime
import time
import sys
from models.zoning import *




parser = argparse.ArgumentParser()
parser.add_argument("camera_id")
args = parser.parse_args()


client = MongoClient('localhost', 27017)
db = client.testdb
cameras = db.AINET_camera
camera = cameras.find_one({'id':int(args.camera_id)})


#THIS IS GONNA BE SUBSTITUTED BY CAM IP
if 'ab-easy' in camera['IP']:
    cap = cv2.VideoCapture('videos/ab-easy2.mp4')
else:    
    cap = cv2.VideoCapture(camera['IP'])
ret, frame = cap.read()
            
try:
    line = draw_boundary(frame)
    direction = ""
    while True:
        direction = input('Specify entry direction :')
        if direction in ["L-R", "R-L", "U-D", "D-U"]:
            break

    cameras.update_one({"id":int(args.camera_id)}, {"$set":{"p1_x":int(line[0][0])}})
    cameras.update_one({"id":int(args.camera_id)}, {"$set":{"p1_y":int(line[0][1])}})
    cameras.update_one({"id":int(args.camera_id)}, {"$set":{"p2_x":int(line[1][0])}})
    cameras.update_one({"id":int(args.camera_id)}, {"$set":{"p2_y":int(line[1][1])}})
    cameras.update_one({"id":int(args.camera_id)}, {"$set":{"IOdirection":direction}})
except Exception as e:
    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)    
