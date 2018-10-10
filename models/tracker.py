import cv2
import math
import numpy
import sys
import time
import datetime

from dbhandler import *

ID = 0

class tracker():
    def __init__(self, a_coord, ID):
        self.x = a_coord[0]
        self.y = a_coord[1]
        self.i = a_coord[2]
        self.p_positions = []
        self.ID = ID
        self.updated = True
        self.image = a_coord[3]
        self.speed = 0
        self.avg_speed = 0
        self.p_positions.append(a_coord)
        #self.birth = time.time()

    def update_position(self, a_coord):
        self.updated = True
        self.x = a_coord[0]
        self.y = a_coord[1]
        self.i = a_coord[2]
        self.image = a_coord[3]
        self.p_positions.append(a_coord)

    def update_tracker(self):
        #This is responsible for the lifespan of the tracker
        self.updated = False
        positions = []
        for x in range(0, len(self.p_positions)):
            lst = list(self.p_positions[x])
            lst[2] -= 0.25
            if lst[2] == 0:
            #if time.time() - self.birth > 4:
                positions.append(x)
            else:    
                self.p_positions.remove(self.p_positions[x])
                self.p_positions.insert(x, tuple(lst))
        for p in positions:
            self.p_positions.remove(self.p_positions[p])


    def current_speed(self):
        distance = math.sqrt((self.x - self.p_positions[len(self.p_positions)][0])**2 + (self.y - self.p_positions[len(self.p_positions)][1])**2)
        self.speed = abs(distance)


    def average_speed(self):
        distance = 0
        i = len(self.p_positions)
        while i != 0:
            distance += math.sqrt((self.p_positions[i][0] - self.p_positions[i-1][0])**2 + (self.p_positions[i][1] - self.p_positions[i-1][1])**2)
            i -= 1
        self.avg_speed = distance/len(self.p_positions)            




def localize(trackers_list):
    #Updates the trackers at the start of the frame, this allows dead trackers to be cleaned
    if trackers_list:
        for x in trackers_list:
            x.update_tracker()


def updater(trackers_list, new_positions, distance):
    #Updates trackers with new positions or creates new ones
    updated_positions = new_positions
    distances = []
    if trackers_list and new_positions:
        for t in trackers_list:
            distances = []
            for p in updated_positions:
                distances.append(math.sqrt((p[0] - t.x)**2 + (p[1] - t.y)**2))
            if min(distances) <= distance:
                t.update_position(updated_positions[distances.index(min(distances))])
                updated_positions.remove(updated_positions[distances.index(min(distances))])
        for p in updated_positions:            
            trackers_list.append(tracker(p, id_generator()))            
        return trackers_list
    
    elif not trackers_list and new_positions:
        for y in new_positions:
            trackers_list.append(tracker(y, id_generator()))
        return trackers_list
    
    else:
        return trackers_list
            

def cleaner(trackers_list):
    #Cleans dead trackers
    if trackers_list:
        for x in trackers_list:
            if not x.p_positions:
                trackers_list.remove(x)
        return trackers_list
    else:
        return trackers_list

def lockon(trackers_list, img):
    if trackers_list:
        for x in trackers_list:
            x.track(img)


def track(trackers_list):
    positions = []
    for t in trackers_list:
        for x in t.p_positions:
            positions.append((x[0], x[1], x[2], t.ID))
    return positions
    
def track_main(trackers_list):
    positions = []
    for t in trackers_list:
        if t.updated:
            positions.append((t.x, t.y, t.i, t.ID))
    return positions  


def ccw(A,B,C):
    #return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])	

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)	    

def trajectory(direction, camera, trackers_list, img, zone, out):
    for t in trackers_list:
        if len(t.p_positions) > 1:
            for i in range(0, len(t.p_positions)-1):
                if out:
                    cv2.line(img, (int(t.p_positions[i][0]), int(t.p_positions[i][1])),
                    (int(t.p_positions[i+1][0]), int(t.p_positions[i+1][1])),
                    (255,0,0), 3)
                if zone:
                    if i == len(t.p_positions)-2:
                        '''line_intersection((((int(t.p_positions[i][0]), int(t.p_positions[i][1]))), 
                        ((int(t.p_positions[i+1][0]), int(t.p_positions[i+1][1])))),
                        ((zone[0][0], zone[0][1]), (zone[1][0], zone[1][1])))'''
                        line1 = [[int(t.p_positions[i][0]), int(t.p_positions[i][1])],[int(t.p_positions[i+1][0]), int(t.p_positions[i+1][1])]]
                        line2 = [[zone[0][0], zone[0][1]],[zone[1][0], zone[1][1]]]
                        A = (int(t.p_positions[i][0]), int(t.p_positions[i][1]))
                        B = (int(t.p_positions[i+1][0]), int(t.p_positions[i+1][1]))
                        C = (zone[0][0], zone[0][1])
                        D = (zone[1][0], zone[1][1])
                        if intersect(A,B,C,D):
                            #print("WE HAVE AN INTERSECTION------------------------")                           
                            #direction = "U-D"
                            if direction == "L-R":
                                if t.p_positions[len(t.p_positions)-1][0] - t.p_positions[len(t.p_positions)-2][0] < 0 :
                                    db_insert(camera, t, "Entrée") 
                                else:
                                    db_insert(camera, t, "Sortie")
                            elif direction == "R-L":
                                if t.p_positions[len(t.p_positions)-1][0] - t.p_positions[len(t.p_positions)-2][0] > 0 : 
                                    db_insert(camera, t, "Entrée")  
                                else:
                                    db_insert(camera, t, "Sortie")
                            elif direction == "U-D":
                                if t.p_positions[len(t.p_positions)-1][1] - t.p_positions[len(t.p_positions)-2][1] > 0 :
                                    db_insert(camera, t, "Entrée")
                                else:
                                    db_insert(camera, t, "Sortie")
                            elif direction == "D-U":
                                if t.p_positions[len(t.p_positions)-1][1] - t.p_positions[len(t.p_positions)-2][1] < 0 :
                                    db_insert(camera, t, "Entrée")
                                else:
                                    db_insert(camera, t, "Sortie")
                                #ADD INTERSECTION CHECK  

def snapshot(t):
    #roi = display_img[y1:y2, x1:x2]
    print(t.image)
    d = time.strftime('%X %x %Z')
    print(d)
    cv2.imwrite(d+".jpg", t.image)

def id_generator():
    global ID
    ID += 1
    return ID
