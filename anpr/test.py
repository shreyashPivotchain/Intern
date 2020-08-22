import cv2
from detect_object_m1 import get_object_bbox_m1
import argparse,time

parser = argparse.ArgumentParser(description='Perimeter Breach')
video = parser.add_argument('--video', help='video')
args = parser.parse_args()
video_file = args.video

cap = cv2.VideoCapture(video_file)
#cap=cv2.VideoCapture('/home/abhishek/Downloads/homeland/annotation/Assault003_x264.mp4')
#cap=cv2.VideoCapture('/home/abhishek/Downloads/homeland/annotation/RoadAccidents031_x264.mp4')
#cap = cv2.VideoCapture('/home/abhishek/Downloads/homeland/accident.mp4')
#cap = cv2.VideoCapture('/home/abhishek/Downloads/homeland/annotation/RoadAccidents039_x264.mp4')
#cap = cv2.VideoCapture('/home/abhishek/Downloads/homeland/annotation/RoadAccidents012_x264.mp4')
#cap = cv2.VideoCapture('/home/abhishek/Downloads/homeland/annotation/Assault047_x264.mp4')
#cap = cv2.VideoCapture('/home/abhishek/Downloads/homeland/data/RoadAccidents/RoadAccidents071_x264.mp4')
#cap = cv2.VideoCapture('/home/abhishek/Downloads/homeland/data/RoadAccidents/RoadAccidents140_x264.mp4')
#cap = cv2.VideoCapture('/home/abhishek/Downloads/homeland/data/Assault/Assault041_x264.mp4')
#cap = cv2.VideoCapture('/home/abhishek/Downloads/homeland/annotation/RoadAccidents010_x264.mp4')
#cap = cv2.VideoCapture('/home/abhishek/Downloads/homeland/fight.mp4')
count=0
while True:
	_,frame=cap.read()
	if count%1==0:
		bboxs=get_object_bbox_m1(frame)
		for bbox in bboxs:
			cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (255,255,255), 2)
			cv2.putText(frame,bbox[-1],(int(bbox[0]), int(bbox[1])),0, 0.5, (0,255,0),2)
		frame = cv2.resize(frame,(640,480))
		cv2.imshow('res1',frame)
#		cv2.imwrite('./images/'+str(count).zfill(9)+'.jpg',frame)
	
	#cv2.putText(frame,'test',(40, 40),0, 5e-3 * 200, (0,255,0),2)
	#cv2.imshow('res',frame)
#	cv2.imwrite('./images3/'+str(count).zfill(9)+'.jpg',frame)
	count+=1
	if cv2.waitKey(1) & 0xFF == ord('q'): 
		break
