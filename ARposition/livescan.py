import cv2
import numpy as np

aruco = cv2.aruco

# マーカー種類を定義
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()

# ArucoDetectorオブジェクトを作成
detector = aruco.ArucoDetector(dictionary, parameters)

# Webカメラをキャプチャ
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

if not cap.isOpened():
    print("Webカメラが見つかりません")
    exit()

while True:
    # フレームを取得
    ret, frame = cap.read()
    if not ret:
        break

    # グレースケールに変換
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # マーカーを検出
    corners, ids, rejectedCandidates = detector.detectMarkers(gray)

    # 検出したマーカーを描画
    if ids is not None:
        frame = aruco.drawDetectedMarkers(frame, corners, ids)
        print(f"検出されたマーカーID: {ids.flatten()}")
        print(corners)

    # フレームを表示
    cv2.imshow('frame', frame)

    # 'q'キーで終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# リソースを解放
cap.release()
cv2.destroyAllWindows()