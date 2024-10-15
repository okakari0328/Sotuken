import cv2
import time
import datetime
import numpy
"""
# カメラを開く
cap = cv2.VideoCapture(0)

ret, frame = cap.read()
tintime = datetime.datetime.now()
filename = tintime.strftime('%Y%m%d_%H%M%S') + '.jpg'
cv2.imwrite(filename, frame)
"""


"""


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


    # フレームを表示
    cv2.imshow('frame', frame)
    key = cv2.waitKey(1) & 0xFF
    # 'q'キーで終了
    if key == ord('z'):
        tintime = datetime.datetime.now()
        filename = tintime.strftime('%Y%m%d_%H%M%S') + '.jpg'
        cv2.imwrite(filename, frame)
    elif key == ord('q'):
        break

# リソースを解放
cap.release()
cv2.destroyAllWindows()
