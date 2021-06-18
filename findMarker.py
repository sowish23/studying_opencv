import os
import math
import cv2 
import subprocess
from PIL import Image
import numpy as np
from pytesseract import *
import sqlite3

conn = sqlite3.connect("test.db", isolation_level=None)

c = conn.cursor()

def setLabel(img, pts, label) :
    (x, y, w, h) = cv2.boundingRect(pts)
    pt1 = (x, y)
    pt2 = (x + w, y + h)
    cv2.rectangle(img, pt1, pt2, (0, 255, 0), 2)
    cv2.putText(img, label, (pt1[0], pt1[1]-3), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255))

img_original = cv2.imread('marker_example3.png', cv2.IMREAD_COLOR)
img_resize = cv2.resize(img_original, dsize=(328, 207), interpolation=cv2.INTER_AREA)
img_dia = img_resize[:180, :190]
gray = cv2.cvtColor(img_dia, cv2.COLOR_BGR2GRAY)
n_white_pix = np.sum(img_resize == 255)
print('Number of white pixels:', n_white_pix)

ret, thr = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)

contours, _ = cv2.findContours(thr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

address = ''

for cont in contours:
    approx = cv2.approxPolyDP(cont, cv2.arcLength(cont, True) * 0.02, True)
    vtc = len(approx)
    if vtc == 3:
        setLabel(img_dia, cont, 'Tri')
        # address = '서울시 성북구 성북로 11길 25'
    elif vtc == 4:
        setLabel(img_dia, cont, 'Rec')
        # address = '서울시 성북구 성북로 12길'
    elif vtc == 5:
        setLabel(img_dia, cont, 'Diamond')
        # address = '서울시 성북구 성북로 13길 13'
    elif vtc == 10:
        setLabel(img_dia, cont, 'Star')
        # address = '서울시 성북구 성북로 13길 8'
    else:
        area = cv2.contourArea(cont)
        _, radius = cv2.minEnclosingCircle(cont)
        ratio = radius * radius * math.pi / area

        if int(ratio) == 1:
            setLabel(img_dia, cont, 'Cir')
            setLabel(img, cont, 'Cir')
    
    c.execute('SELECT * FROM shapeTable WHERE code='+str(vtc))
    print('param2', c.fetchall())

cv2.imshow('img', img_resize)
cv2.imshow('binary', thr)

img_text = img_resize[:, 150:]
text = pytesseract.image_to_string(img_text,lang='eng')

c.execute("SELECT * FROM ocrTable WHERE code='{}'".format(text.strip()))
print('param2', c.fetchall())

# if text.rstrip() == 'ABCD' :
#     address += ' 2층 회의실 A구역'
# elif text.rstrip() == 'ABCE' : 
#     address += ' 2층 탕비실'
# elif text.rstrip() == 'ABCF' : 
#     address += ' 2층 장비실'
# elif text.rstrip() == 'ABCG' : 
#     address += ' 2층 대표실'
# elif text.rstrip() == 'ABCH' : 
#     address += ' 2층 연구실'

cv2.waitKey()
cv2.destroyAllWindows()