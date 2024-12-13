import cv2
import mediapipe as mp
import datetime
import numpy as np
import matplotlib.pyplot as plt

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)

camera_matrix = np.array([[911.16249123, 0, 654.12634946],
                          [0, 956.34794313, 385.3495122],
                          [0, 0, 1]], dtype=float)
dist_coeffs = np.array([ 6.21764090e-01, -1.75458641e+01, -2.07839313e-02, 2.78874705e-03, 1.54224395e+02], dtype=float)
fx = 911.16249123
fy = 956.34794313
cx = 654.12634946
cy = 385.3495122
wid = 640
hei = 480
# 上の数字を使わず、先に計算した逆行列を利用してカメラ座標ベクトルを計算する

#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
landmark_x = [0] * 21
landmark_y = [0] * 21
with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
    ) as hands:

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
                    landmark_x_tmp = hand_landmarks.landmark[id].x
                    landmark_y_tmp = hand_landmarks.landmark[id].y

                    landmark_x[id] = int(landmark_x_tmp * wid)
                    landmark_y[id] = int(landmark_y_tmp * hei)
                    
                    
                    print('x')
                    print(landmark_x)
                    print('y')
                    print(landmark_y)

        cv2.imshow('media', image)
        key = cv2.waitKey(1) & 0xFF
    # 'q'キーで終了
        if key == ord('z'):
            tintime = datetime.datetime.now()
            filename = tintime.strftime('%Y%m%d_%H%M%S') + '.jpg'
            cv2.imwrite(filename, frame)
        elif key == ord('q'):
            break

plt.cla()
plt.clf()
plt.close()
cap.release()
cv2.destroyAllWindows()