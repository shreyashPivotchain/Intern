from PIL import Image, ImageDraw, ImageFont
import tensorflow as tf
import numpy as np
import time
import cv2


def realtime_detection(camera_id, model_file_path):# function
    threshold = 0.5 #cutoff decides which probability of object to detect 50% sured object will will be detected

    with tf.Session() as sess:# to create session and computing graphs and data flow betn the operations
        with tf.gfile.FastGFile(model_file_path, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            tf.import_graph_def(graph_def, name='')

        graph = tf.get_default_graph()
        num = graph.get_tensor_by_name('num_detections:0')
        scores = graph.get_tensor_by_name('detection_scores:0')
        boxes = graph.get_tensor_by_name('detection_boxes:0')
        classes = graph.get_tensor_by_name('detection_classes:0')

        classnames = []
        with open('coco91.names', encoding='utf-8') as f:
            for name in f:
                classnames.append(name.split('\n')[0])

        cap = cv2.VideoCapture(camera_id)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        while cap.isOpened():
            _, frame = cap.read()
            height, width = frame.shape[:2]

            start = time.time()

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)#changing
            out = sess.run([num, scores, boxes, classes], feed_dict={'image_tensor:0': [rgb_frame]})
            #print(out)

            for i in range(int(out[0][0])):
                score = float(out[1][0][i])

                if score > threshold:
                    classid = int(out[3][0][i])

                    left = int(out[2][0][i][1] * width)
                    top = int(out[2][0][i][0] * height)
                    right = int(out[2][0][i][3] * width)
                    bottom = int(out[2][0][i][2] * height)

                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 1)
                    pilimg = Image.fromarray(frame)
                    draw = ImageDraw.Draw(pilimg)
                    font = ImageFont.truetype("simhei.ttf", (bottom - top) // 8)
                    draw.text((left, top), classnames[classid] + str(round(score, 2)), (255, 255, 255), font=font)
                    frame = np.array(pilimg)

            print('object：%f' % ((time.time() - start) * 1000) + 'ms')


            cv2.imshow('object detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        


    
