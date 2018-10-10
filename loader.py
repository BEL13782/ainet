from pymongo import MongoClient


def load_cameras():
    client = MongoClient('localhost', 27017)
    db = client.testdb
    cameras = db.AINET_camera
    all_cameras = cameras.find()

    operational_cameras = []

    for x in all_cameras:
        print(x)

        id = x['id']
        ip = x['IP']
        port = x['port']
        zone_id = x['zone_id']
        direction = x['IOdirection']

        #Boundaries (Line)
        a = (x['p1_x'], x['p1_y'])
        b = (x['p2_x'], x['p2_y'])
        pts = (a, b)

        cam = {
            'id':id,
            'ip':ip,
            'port':port,
            'zone_id':zone_id,
            'line':pts,
            'direction':direction
        }

        operational_cameras.append(cam)

    
    return operational_cameras    

    