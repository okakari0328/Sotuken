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



print(cv2.getBuildInformation())
while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # 画像をRGBに変換
    far = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Mediapipeで処理
    results = hands.process(far)

    # 画像を元のBGRに戻す
    image = cv2.cvtColor(far, cv2.COLOR_RGB2BGR)

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

    cv2.imshow('frame', image)
    key = cv2.waitKey(1) & 0xFF
    # 'q'キーで終了
    if key == ord('z'):
        tintime = datetime.datetime.now()
        filename = tintime.strftime('%Y%m%d_%H%M%S') + '.jpg'
        cv2.imwrite(filename, image)
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

