import os
import math
import cv2 
import subprocess
from PIL import Image
from pytesseract import *


def setLabel(img, pts, label) :
    (x, y, w, h) = cv2.boundingRect(pts)
    pt1 = (x, y)
    pt2 = (x + w, y + h)
    cv2.rectangle(img, pt1, pt2, (0, 255, 0), 2)
    cv2.putText(img, label, (pt1[0], pt1[1]-3), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255))

img_original = cv2.imread('marker_example2.png', cv2.IMREAD_COLOR)
img_resize = cv2.resize(img_original, dsize=(328, 207), interpolation=cv2.INTER_AREA)
img_dia = img_resize[:200, :200]
gray = cv2.cvtColor(img_dia, cv2.COLOR_BGR2GRAY)

ret, thr = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU) #흰색 제외
# ret, thr = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU) #흰색 물체인식

contours, _ = cv2.findContours(thr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


for cont in contours:
    approx = cv2.approxPolyDP(cont, cv2.arcLength(cont, True) * 0.02, True)
    vtc = len(approx)
    if vtc == 3:
        setLabel(img_dia, cont, 'Tri')
    elif vtc == 4:
        setLabel(img_dia, cont, 'Rec')
    elif vtc == 5:
        setLabel(img_dia, cont, 'Diamond')
    elif vtc == 10:
        setLabel(img_dia, cont, 'Star')
    else:
        area = cv2.contourArea(cont)
        _, radius = cv2.minEnclosingCircle(cont)
        ratio = radius * radius * math.pi / area

        if int(ratio) == 1:
            setLabel(img_dia, cont, 'Cir')

cv2.imshow('img', img_resize)
cv2.imshow('binary', thr)

img_text = img_resize[:, 150:]
text = pytesseract.image_to_string(img_text,lang='eng')

print(text)

# subprocess.call("tesseract marker_example2.png output -l eng", shell=True)

# f = open("./output.txt")
# text_list = f.readlines()

# word = "".join(text_list)
# print(word)
# for line in text_list:
#     line.replace('\n', '')
#     print(line)


cv2.waitKey()
cv2.destroyAllWindows()