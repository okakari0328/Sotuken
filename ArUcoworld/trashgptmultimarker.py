import cv2
import numpy as np
import cv2.aruco as aruco

# ArUco辞書の定義
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
parameters = aruco.DetectorParameters()

# コンポジットマーカーを生成する関数
def create_composite_marker(ids, side_length=200, margin=10):
    num_markers = len(ids)
    markers = [aruco.generateImageMarker(aruco_dict, id, side_length) for id in ids]
    marker_size = side_length + 2 * margin
    composite_image = np.zeros((marker_size, marker_size * num_markers), dtype=np.uint8)
    
    for i, marker in enumerate(markers):
        start_x = i * marker_size + margin
        composite_image[margin:margin+side_length, start_x:start_x+side_length] = marker
        
    return composite_image

# マーカーIDリスト
marker_ids = [10, 20, 30, 40]

# コンポジットマーカーの生成
composite_marker = create_composite_marker(marker_ids)

# コンポジットマーカーの保存
cv2.imwrite('composite_marker.png', composite_marker)

# マーカーの検出と認識
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    
    if ids is not None:
        # マーカーを描画
        frame = aruco.drawDetectedMarkers(frame, corners, ids)
        
        # 各マーカーの位置とIDを取得
        for i, corner in enumerate(corners):
            id = ids[i][0]
            # ここで、各マーカーの情報を用いて一つのマーカーとしての処理を行う
            # 例: 中心位置を計算
            center = np.mean(corner[0], axis=0)
            cv2.circle(frame, tuple(center.astype(int)), 5, (0, 255, 0), -1)
            cv2.putText(frame, str(id), tuple(center.astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        
    cv2.imshow('frame', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
