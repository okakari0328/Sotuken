import cv2
import numpy as np


camera_matrix = np.array([[806.02530003, 0, 311.20867267],
                          [0, 753.39260589, 241.68028089],
                          [0, 0, 1]], dtype=float)
dist_coeffs = np.array([-3.34701294e-01, 1.24171341e+01, 1.31389192e-03, -1.00705953e-02, -1.12565810e+02], dtype=float)


aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # ArUcoマーカーを検出
    corners, ids, rejected = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    if np.all(ids is not None):
        # 各マーカーを処理
        for i in range(len(ids)):
            rvec, tvec, _objPoints = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.05, camera_matrix, dist_coeffs)

            # 画像座標系での2次元座標を表示
            for corner in corners[i][0]:
                cv2.circle(frame, tuple(corner.astype(int)), 5, (0, 255, 0), 2)
                print(f"2D Image Coordinates: {corner}")

            # カメラ座標系での3次元座標を表示
            print(f"3D Camera Coordinates (tvec): {tvec[0][0]}")

            # マーカーの軸を描画
            cv2.drawFrameAxes(frame, camera_matrix, dist_coeffs, rvec, tvec, 0.1)

    # 検出されたマーカーの輪郭を描画
    cv2.aruco.drawDetectedMarkers(frame, corners, ids)

    # 画像を表示
    cv2.imshow('frame', frame)

    # 'q'キーが押されたらループを終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# リソースを解放
cap.release()
cv2.destroyAllWindows()
