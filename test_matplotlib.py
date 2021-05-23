#-*- coding:utf-8 -*-
import cv2
from matplotlib import pyplot as plt # as는 alias 적용시 사용

img = cv2.imread('lena.jpeg', cv2.IMREAD_COLOR) #lena.jpeg 이미지를 cv2모듈의 색을 불러오는 모듈을 사용해 불러온다

plt.imshow(img) #img변수를 새 창을 띄워 보여준다
plt.xticks([]) # x축 눈금
plt.yticks([]) # y축 눈금
plt.show() #