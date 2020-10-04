from object_detector import *
from object_detector import realtime_detection

if __name__ == '__main__':
    realtime_detection('./models/frozen_inference_graph.pb')
