#!/usr/bin/env python3
# coding: utf-8

import cv2
from cv2 import aruco

# get dicionary and get parameters
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()

# read from image
input_file = "marker_0.png"
output_file = "detected_marker_0.png"
input_img = cv2.imread(input_file)

# detect and draw marker's information
corners, ids, rejectedCandidates = aruco.detectMarkers(input_img, dictionary, parameters=parameters)
print(ids)
ar_image = aruco.drawDetectedMarkers(input_img, corners, ids)

cv2.imwrite(output_file, ar_image)
