import cv2
import time
# カメラを開く
cap = cv2.VideoCapture(0)
captureimage = 0
while captureimage < 15:
  startSec = time.time()

  # 1.5 秒 止める
  time.sleep(3)

  # 画像をキャプチャする
  ret, frame = cap.read()
  
  # 画像を保存する
  cv2.imwrite("image1.jpg", frame)

  captureimage += 1

# カメラを閉じる
cap.release()


"""
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
"""