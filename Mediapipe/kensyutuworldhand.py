import cv2
import mediapipe as mp
import datetime
import numpy as np
from typing import Optional, cast
import matplotlib.pyplot as plt

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
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
                '''
                for id, lm in enumerate(hand_landmarks.landmark):print(type(oee))
                    h, w, c = image.shape
                    cx, cy, cz = int(lm.x * w), int(lm.y * h), lm.z
                    #print(f'カメラ座標系 - Landmark {id}: (X: {cx}, Y: {cy}, Z: {cz})')
                '''
        if results.multi_hand_world_landmarks:
            for hand_world_landmarks in results.multi_hand_world_landmarks: 
                print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                '''
                landmark_x = [0] * 21
                landmark_y = [0] * 21
                landmark_z = [0] * 21
                
                for id, lm in enumerate(hand_world_landmarks.landmark):
                    landmark_x_tmp = hand_world_landmarks.landmark[id].x
                    landmark_y_tmp = hand_world_landmarks.landmark[id].y
                    landmark_z_tmp = hand_world_landmarks.landmark[id].z
                    landmark_x[id] = int(landmark_x_tmp * 1000)
                    landmark_y[id] = int(landmark_y_tmp * 1000)
                    landmark_z[id] = int(landmark_z_tmp * 1000)
                    print("上から x,y,z")
                    print(landmark_x)
                    print(landmark_y)
                    print(landmark_z)
                    
                    
                    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'projection': '3d'})
                    ax.scatter(landmark_x, landmark_y, landmark_z)
                    ax.set_xlabel("x")
                    ax.set_ylabel("y")
                    ax.set_zlabel("z")
                    plt.show()
                    #print(results.multi_hand_world_landmarks.hand_world_landmarks[landmark[x]])
                    #print(id)
                    #print(lm)
                    #print(f'世界座標系 - Landmark {id}: (X: {int(lm.x * 1000)}, Y: {int(lm.y * 1000)}, Z: {int(lm.z * 1000)})')
                    tri_point1= hand_world_landmarks.landmark[0]    
                    tri_point2= hand_world_landmarks.landmark[5]
                    tri_point3= hand_world_landmarks.landmark[17]
                    print(f'世界座標系 - Landmark {0}: (X: {int(tri_point1.x * 1000)}, Y: {int(tri_point1.y * 1000)}, Z: {int(tri_point1.z * 1000)})')
                    print(f'世界座標系 - Landmark {5}: (X: {int(tri_point2.x * 1000)}, Y: {int(tri_point2.y * 1000)}, Z: {int(tri_point2.z * 1000)})')
                    print(f'世界座標系 - Landmark {17}: (X: {int(tri_point3.x * 1000)}, Y: {int(tri_point3.y * 1000)}, Z: {int(tri_point3.z * 1000)})')
                    '''
                    #https://github.com/google-ai-edge/mediapipe/blob/master/docs/solutions/hands.md
                    #print('none')
                    #print(mp.HandLandmarkerResult())
        
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
