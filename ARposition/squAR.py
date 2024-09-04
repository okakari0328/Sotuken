import cv2
import numpy as np


aruco = cv2.aruco
p_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
marker =  [0] * 4 # 初期化
for i in range(len(marker)):
  marker[i] = aruco.generateImageMarker(p_dict, i, 75) # 75x75 px drawmaker -> generateImageMaker
  cv2.imwrite(f'marker{i}.png', marker[i])
