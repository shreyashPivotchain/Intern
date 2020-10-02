from object_detector import *
from object_detector import realtime_detection

if __name__ == '__main__':
    realtime_detection(0, './models/faster_rcnn_resnet101_coco_2018_01_28.pb')