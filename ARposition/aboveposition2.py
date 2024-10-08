aruco = cv2.aruco
p_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
img = cv2.imread('inu.jpg')
corners, ids, rejectedImgPoints = aruco.detectMarkers(img, p_dict) # 検出

# ここを変更
corners2 = [np.empty((1,4,2))]*4
for i,c in zip(ids.ravel(), corners):
  corners2[i] = c.copy()
m[0] = corners2[0][0][2]
m[1] = corners2[1][0][3]
m[2] = corners2[2][0][0]
m[3] = corners2[3][0][1]

width, height = (500,500) # 変形後画像サイズ
marker_coordinates = np.float32(m)
true_coordinates   = np.float32([[0,0],[width,0],[width,height],[0,height]])
trans_mat = cv2.getPerspectiveTransform(marker_coordinates,true_coordinates)
img_trans = cv2.warpPerspective(img,trans_mat,(width, height))
cv2_imshow( img_trans)
