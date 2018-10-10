import numpy as np
import cv2

btn_down = False

def get_points(im):
    # Set up data to send to mouse handler
    data = {}
    data['im'] = im.copy()
    data['lines'] = []

    # Set the callback function for any mouse event
    cv2.imshow("Image", im)
    cv2.setMouseCallback("Image", mouse_handler, data)
    cv2.waitKey(0)

    # Convert array to np.array in shape n,2,2
    points = np.uint16(data['lines'])

    return points, data['im']

def mouse_handler(event, x, y, flags, data):
    global btn_down

    if event == cv2.EVENT_LBUTTONUP and btn_down:
        #release the button to finish the line
        btn_down = False
        data['lines'][0].append((x, y)) #append the second point
        cv2.circle(data['im'], (x, y), 3, (0, 0, 255),5)
        cv2.line(data['im'], data['lines'][0][0], data['lines'][0][1], (0,0,255), 2)
        cv2.imshow("Image", data['im'])

    elif event == cv2.EVENT_MOUSEMOVE and btn_down:
        #line visualization
        image = data['im'].copy()
        cv2.line(image, data['lines'][0][0], (x, y), (0,0,0), 1)
        cv2.imshow("Image", image)

    elif event == cv2.EVENT_LBUTTONDOWN and len(data['lines']) < 2:
        btn_down = True
        data['lines'].insert(0,[(x, y)]) #prepend the point
        cv2.circle(data['im'], (x, y), 3, (0, 0, 255), 5, 16)
        cv2.imshow("Image", data['im'])


def draw_boundary(img):
    #img = cv2.imread(img, 1)
    pts, final_image = get_points(img)
    cv2.imshow('Image', final_image)
    print (pts)
    print(type(pts))
    print(len(pts))
    a = (pts[1][0][0], pts[1][0][1])
    b = (pts[1][1][0], pts[1][1][1])
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return (a, b)

def define_restricted_area(img):
    bbox = cv2.selectROI(img, False)
    return bbox 

def check_inside_restricted_area(p1, r):
    if r[0] < p1[0] < (r[0]+r[2]) and r[1] < p1[1] < (r[1]+r[3]):
        print('INSIDE')	    