import cv2
import numpy as np

img = cv2.imread('baseball-player.jpg')
b, g, r= cv2.split(img)
img = cv2.merge((r,g,b))
ball = img[409:454, 817:884] # img[행의 시작점: 행의 끝점, 열의 시작점: 열의 끝점]
img[470:515,817:884] = ball # 동일 영역에 Copy
cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()