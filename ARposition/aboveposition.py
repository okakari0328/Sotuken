import cv2
import numpy as np


aruco = cv2.aruco
p_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
img = cv2.imread('Naname.jpeg')
corners, ids, rejectedImgPoints = aruco.detectMarkers(img, p_dict) # 検出

# 時計回りで左上から順にマーカーの「中心座標」を m に格納
m = np.empty((4,2))
for i,c in zip(ids.ravel(), corners):
  m[i] = c[0].mean(axis=0)

width, height = (500,500) # 変形後画像サイズ

marker_coordinates = np.float32(m)
true_coordinates   = np.float32([[0,0],[width,0],[width,height],[0,height]])
trans_mat = cv2.getPerspectiveTransform(marker_coordinates,true_coordinates)
img_trans = cv2.warpPerspective(img,trans_mat,(width, height))
cv2.imshow('camera', img_trans) #わかんないめう

