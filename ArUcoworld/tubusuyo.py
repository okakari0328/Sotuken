import cv2
import numpy as np

# カメラキャリブレーションパラメータ
camera_matrix = np.array([[806.02530003, 0, 311.20867267],
                          [0, 753.39260589, 241.68028089],
                          [0, 0, 1]], dtype=float)
dist_coeffs = np.array([-3.34701294e-01, 1.24171341e+01, 1.31389192e-03, -1.00705953e-02, -1.12565810e+02], dtype=float)

# ArUcoマーカーの辞書と検出パラメータ
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()

# カメラ映像の取得
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # グレースケール変換
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # マーカーの検出
    corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    if ids is not None:
        # 姿勢推定
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, 0.05, camera_matrix, dist_coeffs)

        for i in range(len(ids)):
            rvec, tvec = rvecs[i], tvecs[i]

            # 回転行列に変換
            rotation_matrix, _ = cv2.Rodrigues(rvec)
            print(f"Marker ID: {ids[i]}")
            print(f"Rotation Vector:\n{rvec}")
            print(f"Translation Vector:\n{tvec}")
            print(f"Rotation Matrix:\n{rotation_matrix}")


    # マーカーの描画
    cv2.aruco.drawDetectedMarkers(frame, corners, ids)

    cv2.imshow('ArUco Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
