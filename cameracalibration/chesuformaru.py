import cv2
import numpy as np
import os
import glob
from matplotlib import pyplot as plt

# Defining the dimensions of checkerboard
CHECKERBOARD = (4,6)

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# cv2.TERM_CRITERIA_EPS:指定された精度(epsilon)に到達したら繰り返し計算を終了する
# cv2.TERM_CRITERIA_MAX_ITER:指定された繰り返し回数(max_iter)に到達したら繰り返し計算を終了する
# cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER : 上記のどちらかの条件が満たされた時に繰り返し計算を終了する
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Defining the world coordinates for 3D points
objp = np.zeros((1, CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
prev_img_shape = None

file_name = glob.glob('calibimageformaru/*.jpg')[0]
img = cv2.imread(file_name)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# Find the chess board corners
# If desired number of corners are found in the image then ret = true
ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH+cv2.CALIB_CB_FAST_CHECK+cv2.CALIB_CB_NORMALIZE_IMAGE)

# Creating vector to store vectors of 3D points for each checkerboard image
objpoints = []

# Creating vector to store vectors of 2D points for each checkerboard image
imgpoints = [] 

if ret == True:
    objpoints.append(objp)
    
    # refining pixel coordinates for given 2d points.
    corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
    
    imgpoints.append(corners2)
    
    # Draw and display the corners
    img = cv2.drawChessboardCorners(img, CHECKERBOARD, corners2,ret)
    

cv2.imwrite('./seigyotenn.jpg',cv2.cvtColor(img, cv2.COLOR_BGR2RGB)) # OpenCV は色がGBR順なのでRGB順に並べ替える


"""
Performing camera calibration by 
passing the value of known 3D points (objpoints)
and corresponding pixel coordinates of the 
detected corners (imgpoints)
"""
h,w = img.shape[:2]
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

# Using the derived camera parameters to undistort the image


# Refining the camera matrix using parameters obtained by calibration
# ROI:Region Of Interest(対象領域)
# カメラ行列(内部パラメータ)を改善する関数
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

# Method 1 to undistort the image
# 歪み補正を行う関数
dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

cv2.imwrite('./calib.jpg',cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)) # OpenCV は色がGBR順なのでRGB順に並べ替える


print("Camera matrix : \n")
print(mtx)
print("dist : \n")
print(dist)
print("rvecs : \n")
print(rvecs)
print("tvecs : \n")
print(tvecs)

fovx, fovy, focal_length, principal_point, aspect_ratio = cv2.calibrationMatrixValues(mtx,(800, 600), 5.6, 4.2)
#カメラのページより、イメージセンサは1/2.5型。
print("水平軸に沿った画角 : \n")
print(fovx)
print("垂直軸に沿った画角 : \n")
print(fovy)
print("焦点距離 : \n")
print(focal_length)
print("ピクセル単位で表された主点 : \n")
print(principal_point)
print("アスペクト比 : \n")
print(aspect_ratio)
