import cv2
import mediapipe as mp
import random
import time


# MediaPipeのHand Trackingインスタンスを作成
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


# 画面の幅と高さ
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480


# 円の中心座標と半径
CIRCLE_CENTER = (int(WINDOW_WIDTH/2), int(WINDOW_HEIGHT/2))
CIRCLE_RADIUS = 50


# ポイントと制限時間の初期化
points = 0
time_limit = 30
start_time = time.time()
game_started = False


# Webカメラの初期化
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WINDOW_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, WINDOW_HEIGHT)


with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5) as hands:


    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break


        # 画像を水平方向に反転してミラー表示
        frame = cv2.flip(frame, 1)


        # ゲームが開始していない場合はスタート画面を表示
        if not game_started:
            cv2.putText(frame, "Press Enter to Start", (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow('Hand Detection', frame)


            # キー入力を待機してゲームを開始
            key = cv2.waitKey(1)
            if key == 13:  # Enterキー
                game_started = True
                start_time = time.time()


            continue


        # 入力画像をMediaPipeに渡して手の位置を検出
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)


        # 手の位置が検出された場合
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # 手の位置を描画
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=4),
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
                )


                # 手の中心座標を取得
                cx = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * WINDOW_WIDTH)
                cy = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * WINDOW_HEIGHT)


                # 円の中に手が入ったか判定
                dist = ((cx - CIRCLE_CENTER[0]) ** 2 + (cy - CIRCLE_CENTER[1]) ** 2) ** 0.5
                if dist < CIRCLE_RADIUS:
                    points+= 1


                    # 円の位置をランダムに変更
                    CIRCLE_CENTER = (random.randint(CIRCLE_RADIUS, WINDOW_WIDTH - CIRCLE_RADIUS),random.randint(CIRCLE_RADIUS, WINDOW_HEIGHT - CIRCLE_RADIUS))


        # 円を描画
        cv2.circle(frame, CIRCLE_CENTER, CIRCLE_RADIUS, (255, 0, 0), 2)


        # ポイントと残り時間を表示
        cv2.putText(frame, f"Points: {points}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        elapsed_time = time.time() - start_time
        remaining_time = max(time_limit - int(elapsed_time), 0)
        cv2.putText(frame, f"Time: {remaining_time}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


        # 制限時間を超えた場合は結果表示画面を表示
        if elapsed_time >= time_limit:
            cv2.putText(frame, "Game Over", (250, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(frame, f"Points: {points}", (280, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow('Hand Detection', frame)


            # キー入力を待機して終了
            key = cv2.waitKey(0)
            if key == 27:  # Escキー
                break


            # ゲームをリセット
            points = 0
            start_time = time.time()
            game_started = False


        cv2.imshow('Hand Detection', frame)


        if cv2.waitKey(10) & 0xFF == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()