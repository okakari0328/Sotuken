import cv2
import mediapipe as mp
import datetime

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("カメラからフレームを取得できませんでした")
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)

        results = hands.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                for id, lm in enumerate(hand_landmarks.landmark):
                    h, w, c = image.shape
                    cx, cy, cz = int(lm.x * w), int(lm.y * h), lm.z
                    #print(f'カメラ座標系 - Landmark {id}: (X: {cx}, Y: {cy}, Z: {cz})')

        if results.multi_hand_world_landmarks:
            for hand_world_landmarks in results.multi_hand_world_landmarks:
                
                    lm = hand_world_landmarks.landmark[4]
                    print(f'世界座標系 - Landmark {4}: (X: {int(lm.x * 1000)}, Y: {int(lm.y * 1000)}, Z: {int(lm.z * 1000)})')
                    #print('none')
                    #qprint(mp.HandLandmarkerResult())
        key = cv2.waitKey(1) & 0xFF
    # 'q'キーで終了
        if key == ord('z'):
            tintime = datetime.datetime.now()
            filename = tintime.strftime('%Y%m%d_%H%M%S') + '.jpg'
            cv2.imwrite(filename, frame)
        elif key == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
