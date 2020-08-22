import numpy as np
import argparse
import cv2 as cv
import time
#from config import *
import tensorflow as tf

#classNames = {1: "Fuselage", 2: "AIRCRAFT", 3: "PBS", 4: "CONV", 5: "BULK", 6: "TUG",
#              7: "FUEL", 8: "TOW", 9: "CAT", 10: "PER", 11: "BUS", 12: "PickupTruck",
#              13: "CrewVan", 14: "GPU", 15: "AC", 16: "PortableGPU", 17: "CleaningCar",
#              18: "WV/LV", 19: "ContainerLoader", 20: "Truck", 21: "ULDContainer",
#              22: "AS cleaning vehicle", 23: 'Trolley', 24: 'ContainerCarrier', 25: "AS", 26: "PBB",27:'PBB Connected', 28:'CAT Connected', 
#              29:'Cargo Connected', 30:'Cargo Connected', 31:'WV/LV Connected', 32: 'PBS Connected'}
# classNames = { 1: 'person',2:'PLB',3:'conveyor',4:'bulk-train',5:'fuselage',6:'aeroplane',7:'UDCAT',8:'fuel',9:'TOW'}
#classNames = {1:'Arson', 2:'Explosion',3:'Fighting',4:'Road Accident',5:'Robbery'}
#classNames = {1:'Fighting',2:'Road Accident'}
#classNames = {1:'Fighting',2:'Road Accident',3:'Robbery', 4:'Arson', 5:'Explosion', 6:'car'}
#classNames = {1:'Fighting',2:'Road Accident',3:'Arson', 4:'Explosion', 5:'car'}
#classNames = {1:'nine', 2:'ten',3:'jack',4:'queen',5:'king',6:'ace'}
classNames = {1: 'NP'}
'''
classNames={1:"fuselage",
2:"aeroplane",
3:"PLB",
4:"Conveyor",
5:"Bulk Train",
6:"Tugs/Tractors",
7:"Fuel",
8:"Tow",
9:"CAT",
10:"Person",
11:"Passenger Bus",
12:"Pickup trucks",
13:"Crew Vans",
14:"GPU",
15:"Air Conditioning Unit",
16:"Portable GPU",
17:"Cleaning Car",
18:"Potable Water Vehicle",
19:"Container Loader",
20:"Trucks",
21:"ULD Container",
22:"AS cleaning vehicle"}
'''
with tf.gfile.FastGFile('test_model/frozen_inference_graph_45k.pb', 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())

sess= tf.Session()
#print('##########################')
sess.graph.as_default()
#print('##########################')
tf.import_graph_def(graph_def, name='') 
#print('##########################')
#net = cv2.dnn.readNetFromTensorflow(pb_model)
def get_object_bbox_m1(img):
    #if frame.shape==None:
    #    return
    bbox_arr=[]

    #frame_resized = cv2.resize(frame,(300,300))
    #blob = cv2.dnn.blobFromImage(frame_resized, size=(300, 300), swapRB=True, crop=False)
    #Set to network the input blob 
    #net.setInput(blob)
    #Prediction of network
    #if count%2==0:
    # with  as :
        # Restore session
   

    # Read and preprocess an image.
    #img = cv.imread('example.jpg')
    rows = img.shape[0]
    cols = img.shape[1]
    inp = cv.resize(img, (300, 300))
    inp = inp[:, :, [2, 1, 0]]  # BGR2RGB    

    # Run the model
    out = sess.run([sess.graph.get_tensor_by_name('num_detections:0'),
                    sess.graph.get_tensor_by_name('detection_scores:0'),
                    sess.graph.get_tensor_by_name('detection_boxes:0'),
                    sess.graph.get_tensor_by_name('detection_classes:0')],
                   feed_dict={'image_tensor:0': inp.reshape(1, inp.shape[0], inp.shape[1], 3)})    
    # Visualize detected bounding boxes.
    num_detections = int(out[0][0])
    for i in range(num_detections):
        classId = int(out[3][0][i])
        score = float(out[1][0][i])
        bbox = [float(v) for v in out[2][0][i]]
        if score > 0.3:
            print(score)
            x = bbox[1] * cols
            y = bbox[0] * rows
            right = bbox[3] * cols
            bottom = bbox[2] * rows
        # Draw location of object  
        #cv2.rectangle(frame, (xLeftBottom, yLeftBottom), (xRightTop, yRightTop),
        #              (255,150, 100),2)
            bbox_arr.append([x, y,right, bottom,classNames[classId]])
    return bbox_arr



