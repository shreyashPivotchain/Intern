import cv2
from PIL import Image
import  numpy as np
import matplotlib.pyplot as plt

def show_img(img_path,title = ""):
    img = cv2.imread(img_path)
    plt.imshow(img)
    plt.title(title)
    plt.axis("off")

def plot_images(img1, img2, title1="", title2=""):
    fig = plt.figure(figsize=[15,15])
    ax1 = fig.add_subplot(121)
    ax1.imshow(cv2.cvtColor(img1,cv2.COLOR_BGR2RGB))
    ax1.set(xticks=[], yticks=[], title=title1)

    ax2 = fig.add_subplot(122)
    ax2.imshow(cv2.cvtColor(img2,cv2.COLOR_BGR2RGB))
    ax2.set(xticks=[], yticks=[], title=title2)

def extract_plates(image,bboxs):
    text = []
    for i in range(len(bboxs)):
        img  = image[int(bboxs[i][1]):int(bboxs[i][3]),int(bboxs[i][0]):int(bboxs[i][2])]
        img = transform_image(img)
        text.append(predict_text(img))
    
    return img

def transform_image(img):
    img_orig = img.copy()
    img = grayscale(img)
    img = blurred(img)
    img = thresholding(img)
    img = canny(img)
    img = contour(img,img_orig)
    img = deskew(img)
    return img


def grayscale(img):
    return cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

def blurred(img):
    return cv2.medianBlur(img,5)

def thresholding(img):
    return cv2.threshold(img,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

#canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)

def contour(edge,image):
    cnts,new = cv2.findContours(edge.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts,key = cv2.contourArea,reverse=True)[:25]
    plate = None
    for c in cnts:
        perimeter = cv2.arcLength(c, True)
        edges_count = cv2.approxPolyDP(c, 0.02 * perimeter, True)
        if len(edges_count) == 4:
            x,y,w,h = cv2.boundingRect(c)
            plate = image[y:y+h, x:x+w]
            break
    mask = np.zeros(grayscale(image).shape,np.uint8)
    new_img = cv2.drawContours(mask,[edges_count],0,255,-1)
    new_image = cv2.bitwise_and(image,image,mask=mask)
    return new_image

def deskew(image):
    image = grayscale(image)
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated