import matplotlib.pyplot as plt
import numpy as np
import cv2
from detect_object_m1 import get_object_bbox_m1
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"

def plot(img):
    if len(img.shape) == 3:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    
    plt.imshow(img,cmap = "gray")
    plt.axis("off")

def plot_images(img1, img2, title1="", title2=""):
    fig = plt.figure(figsize=[15,15])
    ax1 = fig.add_subplot(121)
    ax1.imshow(cv2.cvtColor(img1,cv2.COLOR_BGR2RGB))
    ax1.set(xticks=[], yticks=[], title=title1)

    ax2 = fig.add_subplot(122)
    ax2.imshow(cv2.cvtColor(img2,cv2.COLOR_BGR2RGB))
    ax2.set(xticks=[], yticks=[], title=title2)



def predict_number_plates(img_path):
    img = cv2.imread(img_path)
    frame = img.copy()
    bboxs = get_object_bbox_m1(frame)
    for bbox in bboxs:
        cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (255,255,255), 2)
        cv2.putText(frame,bbox[-1],(int(bbox[0]), int(bbox[1])),0, 0.5, (0,255,0),2)
    frame = cv2.resize(frame,(640,480))
    plot_images(img,frame,"orig","predicted")
    
    plates = [img[int(bbox_[1]):int(bbox_[3]),int(bbox_[0]):int(bbox_[2])] for bbox_ in bboxs]
    if len(plates) >=2:
        plot_images(plates[0],plates[1],"plates","plates")
    else:
        plot_images(plates[0],plates[0],"plates","plates")

    plates_trans = [identify_plates(plate_) for plate_ in plates]
    if len(plates) >=2:
        plot_images(plates_trans[0],plates_trans[1],"plates_trans","plates_trans")
    else:
        plot_images(plates_trans[0],plates_trans[0],"plates_trans","plates_trans")
    
    texts = [pytesseract.image_to_string(plate_,lang="eng") for plate_ in plates_trans]
    for text in texts:
        print(text)
    return plates_trans,texts,plates


def identify_plates(image) :

    img_lp = cv2.resize(image, (333, 75))
    img_gray_lp = cv2.cvtColor(img_lp, cv2.COLOR_BGR2GRAY)
    _, img_binary_lp = cv2.threshold(img_gray_lp, 200, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    img_binary_lp = cv2.erode(img_binary_lp, (3,3))
    img_binary_lp = cv2.dilate(img_binary_lp, (3,3))

    LP_WIDTH = img_binary_lp.shape[0]
    LP_HEIGHT = img_binary_lp.shape[1]

    img_binary_lp[0:3,:] = 255
    img_binary_lp[:,0:3] = 255
    img_binary_lp[72:75,:] = 255
    img_binary_lp[:,330:333] = 255
    
    return img_binary_lp
