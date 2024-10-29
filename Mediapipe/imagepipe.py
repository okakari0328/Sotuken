import cv2
import mediapipe as mp


# MediaPipeのHandsモジュールを初期化
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

landmark_drawing_spec = mp_draw.DrawingSpec(color=(0, 255, 0), thickness=5, circle_radius=5) # 緑色、太さ5、半径5
connection_drawing_spec = mp_draw.DrawingSpec(color=(255, 0, 0), thickness=3)                # 赤色、太さ3

# 画像のパスを指定
image_path = 'path/to/your/image.jpg'

# 画像を読み込む
image = cv2.imread('./goodhand.jpg')
if image is None:
    print("画像が見つかりません。パスを確認してください。")
    exit()

# 画像をRGBに変換
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# 手のランドマークを検出
results = hands.process(rgb_image)

# 検出結果を描画
if results.multi_hand_landmarks:
    for hand_landmarks in results.multi_hand_landmarks:
        mp_draw.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            landmark_drawing_spec,
            connection_drawing_spec
        )
# 画像を表示
cv2.imwrite("tin.jpg", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
