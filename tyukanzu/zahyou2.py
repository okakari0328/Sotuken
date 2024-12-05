import matplotlib.pyplot as plt
import numpy as np

# 図の作成
fig = plt.figure(figsize=(12, 8))

# 3Dプロット用の設定
ax = fig.add_subplot(111, projection='3d')

# 世界座標系の点
world_points = np.array([
    [0, 0, 0],
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
])
world_points_labels = ['W_origin', 'X_w', 'Y_w', 'Z_w']

# カメラ座標系の点
R = np.eye(3)  # カメラの回転行列（単位行列と仮定）
t = np.array([2, 2, 2])  # カメラの平行移動ベクトル
camera_points = (R @ world_points.T).T + t
camera_points_labels = ['C_origin', 'X_c', 'Y_c', 'Z_c']

# 画像座標系の点（カメラ座標系から投影）
K = np.array([
    [1000, 0, 320],
    [0, 1000, 240],
    [0, 0, 1]
])
image_points = (K @ camera_points.T).T
image_points = image_points[:, :2] / image_points[:, 2, np.newaxis]
image_points_labels = ['I_origin', 'X_i', 'Y_i', 'Z_i']

# 世界座標系のプロット
ax.scatter(world_points[:, 0], world_points[:, 1], world_points[:, 2], color='r')
for i, label in enumerate(world_points_labels):
    ax.text(world_points[i, 0], world_points[i, 1], world_points[i, 2], label)

# カメラ座標系のプロット
ax.scatter(camera_points[:, 0], camera_points[:, 1], camera_points[:, 2], color='b')
for i, label in enumerate(camera_points_labels):
    ax.text(camera_points[i, 0], camera_points[i, 1], camera_points[i, 2], label)

# 画像座標系のプロット
for i, label in enumerate(image_points_labels):
    plt.scatter(image_points[i, 0], image_points[i, 1], color='g')
    plt.text(image_points[i, 0], image_points[i, 1], label, fontsize=12, color='g')

# ラベルの設定
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('World, Camera, and Image Coordinate Systems')

# プロットの表示
plt.show()
