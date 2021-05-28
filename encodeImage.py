import cv2
import numpy as np

path = './image/AATLL.jpg'
with open(path, 'rb') as f:
    data = f.read()
# print('data : ', data)
encoded_img = np.fromstring(data, dtype = np.uint8)


path2 = './image/AATLR.jpg'
with open(path2, 'rb') as f2:
    data2 = f2.read()
# print('data2 : ', data2.typeOf())
encoded_img2 = np.fromstring(data2, dtype = np.uint8)
# print(encoded_img == encoded_img2)
# print(len(encoded_img2))
# img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)   

img_cv = cv2.imread(path)
binary_cv = cv2.imencode('.JPG', img_cv)[1].tobytes()
print(binary_cv[:20])
