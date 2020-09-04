import cv2
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
import re




first_chars = ['A',"B","D","G","H","J","K","L","M","O","P","R","S","T","U","W"]
sec_chars = ['A','B','D','H','J','K','N','P','R','S','T','Y']
ints = ['0','1','2','3','4','5','6','7','8','9']
chars_convt = ['I','L','Z','E','H','A','S','G','T','B','J','O','D','X']

def chars_to_int(i):
    if i in chars_convt:
        if i in ['O','D']:
            return '0'
        if i in ['L','I']:
            return '1'
        if i == 'Z':
            return '2'
        if i == 'E':
            return '3'
        if i in  ['A','H']:
            return '4'
        if i == 'S':
            return '5'
        if i == 'G':
            return '6'
        if i == 'T':
            return '7'
        if i in  ['B','X']:
            return '8'
        if i == 'J':
            return '9'
    else:
        return i


def int_to_char(i):
    if i in ints:
        if i == '0':
            return 'O' 
        if i == '1':
            return 'I'
        if i == '2':
            return 'Z'
        if i == '3':
            return 'B'
        if i == '4':
            return 'A'
        if i == '5':
            return 'S'
        if i == '6':
            return 'G'
        if i == '7':
            return 'T'
        if i == '8':
            return 'B'
        if i == '9':
            return 'J'
    else:
        return i

def first_char(i,check = 0):
    text = []
    if i[0] in first_chars and i[1] not in ints:
        if i[0] == "A":
            if i[1] in ["N","P","R","S"]:
                text[:2] = i[:2]
            elif i[1] in ['W','M','V']:
                text[:2] = i[0] + 'N'
            else:
                text[:2] = i[0] + 'P'
        if i[0] == 'B':
            text[:2] = i[0] + 'R'
        if i[0] == 'D':
            if i[1] in ['D','N','L']:
                text[:2] = i[:2]
            else:
                text[:2] = "DL"
        if i[0] == 'G':
            if i[1] in ['A','J']:
                text[:2] = i[:2]
            elif i[1] == 'H':
                text[:2] = 'GA'
            else:
                text[:2] = 'GJ'
        if i[0] == 'H':
            if i[1] in ['P','R']:
                text[:2] = i[:2]
            else:
                text[:2] = 'HR'
        if i[0] == 'J':
            if i[1] in ['H','K']:
                text[:2] = i[:2]
            elif i[1] in ['X','V','Y']:
                text[:2] = i[0] + 'K'
            else:
                text[:2] = i[0] + 'H'
        if i[0] == 'K':
            if i[1] in ['A','L']:
                text[:2] = i[:2]
            elif i[1] in ['U','I','J','C']:
                text[:2] = i[0] + 'L'
            else:
                text[:2] =  'KA'
        if i[0] == 'M':
            if i[1] in ['P','H','N','L','Z']:
                text[:2] = i[:2]
            elif i[1] in ['R','B']:
                text[:2] = i[0] + 'P'
            else:
                text[:2] =  'MH'
        if i[0] == 'O':
            if i[1] in ['T','P','A','F','K','B','X']:
                text[:2] = i[0] + 'R'
        if i[0] == 'P':
            if i[1] in ['Y','B']:
                text[:2] = i[:2]
            elif i[1] in ['V','U','X','I']:
                text[:2] = 'PY'
            else:
                text[:2] = 'PB'
        if i[0] == 'R':
            text[:2] = 'RJ'
        if i[0] == 'S':
            text[:2] = 'SK'
        
        if i[0] == 'T':
            if i[1] in ['N','G','R','S']:
                text[:2] = i[:2]
            elif i[1] in ['P','B']:
                text[:2] = 'TR'
            else:
                text[:2] = 'TN'
        
        if i[0] == 'U':
            if i[1] in ['P','K']:
                text[:2] = i[:2]
            elif i[1] in ['Y','T','I','V']:
                text[:2] = 'UK'
            else:
                text[:2] = 'UP'
        if i[0] == 'W':
            text[:2] = 'WB'
        check = 1
    else:
        check = 0

    return ''.join(a for a in text),check

def second_char(i,check = 0):
    text = []
    if i[1] in sec_chars:
        if i[1] == "A":
            text[:2] = "KA"
        if i[1] == 'B':
            if i[0] in ['R','T','F','B']:
                text[:2] = 'PB'
            else:
                text[:2] = 'WB'
        if i[1] == 'D':
            text[:2] = 'DD'
        if i[1] == 'H':
            if i[0] in ['U','I','L']:
                text[:2] = 'JH'
            else:
                text[:2] = 'MH'
        if i[1] == 'J':
            if i[0] in ['P','T','A','F','H','B']:
                text[:2] = 'RJ'
            else:
                text[:2] = 'GJ'
        if i[1] == 'K':
            if i[0] in ['U','I','L']:
                text[:2] = 'JK'
            else:
                text[:2] = 'SK'
        if i[1] == 'N':
            text[:2] = 'TN'
        if i[1] == 'P':
            if i[0] in ['R','P','H','F','K']:
                text[:2] = 'AP'
            else:
                text[:2] = 'MP'
        if i[1] == 'R':
            if i[0] in ['U','Q','C','D','G']:
                text[:2] = "OR"
            else:
                text[:2] = 'HR'
        if i[1] == 'S':
            if i[0] in ['I','P','F']:
                text[:2] = 'TS'
            else:
                text[:2] = 'AS'
        check = 1
    else:
        check = 0

    return ''.join(a for a in text),check

def clean_text(txt):
    txt = str(txt)
    np = []
    if len(txt) > 8:
        np[:2] = int_to_char(txt[0]) + int_to_char(txt[1])
        
        txt = "".join(a for a in np) + txt[2:]
        np[:2],check = first_char(txt)
        if not check:
            np[:2],check = second_char(txt)
            if not check:
                np[:2] = txt[:2]
        np[2:4] = chars_to_int(txt[2]) + chars_to_int(txt[3])
        np[4:6] = int_to_char(txt[4]) + int_to_char(txt[5])
        temp = [chars_to_int(a) for a in txt[-(len(txt) - 6):]]
        return "".join(a for a in np) + "".join(a for a in temp)
    else:
        return "unk"

def ocr_1(img_path):
    
    image = cv2.imread(img_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (300, 50), interpolation=cv2.INTER_CUBIC)
    gray_bin = cv2.GaussianBlur(resized, (5, 5), 0)
    txt = pytesseract.image_to_string(gray_bin,lang='eng', config='--oem 3 --psm 6')
    if((len(txt) > 0)and (txt[0].isdigit())):
        txt = txt[1:]
    result = re.sub('[\W_]+', '', txt) 
    result = ''.join(ch for ch in result if (ch.isupper() or ch.isnumeric()))
    return result


def ocr_2(img_path):
    image = cv2.imread(img_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    dn_gray = cv2.fastNlMeansDenoising(resized, templateWindowSize=7, h=25)
    gray_bin = cv2.threshold(dn_gray, 80, 255, cv2.THRESH_BINARY)[1]
    txt = pytesseract.image_to_string(gray_bin,lang='eng', config='--oem 3 --psm 6')
    if((len(txt) > 0)and (txt[0].isdigit())):
        txt = txt[1:]
    result = re.sub('[\W_]+', '', txt) 
    result = ''.join(ch for ch in result if (ch.isupper() or ch.isnumeric()))
    return result

def ocr_3(img_path):
    img = cv2.imread(img_path)
    img_lp = cv2.resize(img, (333, 75))
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
    txt = pytesseract.image_to_string(img_binary_lp,lang='eng')
    if((len(txt) > 0)and (txt[0].isdigit())):
        txt = txt[1:]
    result = re.sub('[\W_]+', '', txt) 
    result = ''.join(ch for ch in result if (ch.isupper() or ch.isnumeric()))
    return result


imgs = os.listdir('cropped')
#df = pd.DataFrame(img_list)
#df['ocr1_'] = ''*len(df)
#df['ocr1_cl'] = ''*len(df)
#df['ocr2_'] = ''*len(df)
#df['ocr2_cl'] = ''*len(df)
df['ocr3_'] = ''*len(df)
df['ocr3_cl'] = ''*len(df)

def get_plates(imgs_list):
    for i,img in enumerate(imgs_list):
        text = ocr_3(img)
        df.iloc[i,5] = text
        text = clean_text(text)
        if text != 'unk':
            df.iloc[i,6] = text

get_plates(imgs)

plates = []
for fle in ['ocr1_','ocr1_cl', 'ocr2_', 'ocr2_cl',
       'ocr3_', 'ocr3_cl']:
       for txt in df[fle][df[fle].notnull()].values:
           check = re.search('[ABCDGHJ-MOPRSTUW][ABDHJKLNPRSTY][0-9]{1,2}[A-Z]{1,3}[0-9]{2,4}',txt)
           if check:
               plates.append(check[0])

def uniq(input):
  output = []
  for x in input:
    if x not in output:
      output.append(x)
  return output

plates_unique = uniq(plates)

with open('plates.txt','w') as output:
    output.write(str(plates_unique))