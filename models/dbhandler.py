from pymongo import MongoClient
from skimage.io import imsave
import datetime
import time
import sys


client = MongoClient('localhost', 27017)
db = client.testdb

def db_insert(camera, tracker, event_type):

    try:
        timestr = time.strftime("%Y%m%d-%H%M%S")
        name = "roi"+timestr+".jpg"
        path = r"D:\ainet\webapp\AINET\static\db_images\roi"+timestr+".jpg"
        imsave(path, tracker.image)
        
        events = db.AINET_event
        events.insert_one({
            "id" : events.count() + 1,
            "type" : event_type,
            "time" : datetime.datetime.now(),
            "image" : name,
            "camera_id" : camera 
        })
        print("Event succesfully inserted")
        
    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

