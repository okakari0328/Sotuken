#pip install openCV-python
#pip install mediapipe
import cv2
import mediapipe as mp
import datetime
# Mediapipeの初期化
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# カメラのキャプチャ
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
cap.set(cv2.CAP_PROP_FPS, 60)           # カメラFPSを60FPSに設定
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) # カメラ画像の横幅を1280に設定
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720) # カメラ画像の縦幅を720に設定
# 各種プロパティーを取得
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # フレームの幅
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # フレームの高さ
fps = float(cap.get(cv2.CAP_PROP_FPS))  # FPS
# 動画保存の設定
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = None
recording = False


print(cv2.getBuildInformation())
while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # 画像をRGBに変換
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Mediapipeで処理
    results = hands.process(image)

    # 画像を元のBGRに戻す
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # 手のランドマークを描画し、座標を取得
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            for idx, landmark in enumerate(hand_landmarks.landmark):
                h, w, _ = image.shape
                cx, cy, cz = int(landmark.x * 100), int(landmark.y * 100), int(landmark.z * 100) 
                print(f'Landmark {idx}: (x: {cx}, y: {cy}, z: {cz})')
                #cx, cy = int(landmark.x * w), int(landmark.y * h)
                #print(f'Landmark {idx}: (x: {cx}, y: {cy})')

    # 結果の表示
    cv2.imshow('Hand Tracking', image)

    # キー入力の処理
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        tintime = datetime.datetime.now()
        filename = tintime.strftime('%Y%m%d_%H%M%S') + '.jpg'
        cv2.imwrite(filename, image)
    elif key == 27:  # ESCキー
        break

cap.release()
cv2.destroyAllWindows()

