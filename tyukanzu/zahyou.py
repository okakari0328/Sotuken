import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def draw_coordinate_system(ax, origin, R, label, color='r'):
    """
    座標系を描画するためのヘルパー関数
    :param ax: matplotlibのAxes3Dオブジェクト
    :param origin: 座標系の原点
    :param R: 回転行列
    :param label: 座標系のラベル
    :param color: 座標軸の色
    """
    # 各軸の描画
    for i in range(3):
        axis = np.zeros((2, 3))
        axis[1, i] = 1
        axis = (R @ axis.T).T + origin
        ax.plot(axis[:, 0], axis[:, 1], axis[:, 2], color=color)
        ax.text(axis[1, 0], axis[1, 1], axis[1, 2], f'{label}{i + 1}', color=color)

# 図の初期化
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 世界座標系の定義
origin_world = np.array([0, 0, 0])
R_world = np.eye(3)

# カメラ座標系の定義
origin_camera = np.array([1, 1, 1])
R_camera = np.array([[0.866, -0.5, 0],
                     [0.5, 0.866, 0],
                     [0, 0, 1]])

# 座標系の描画
draw_coordinate_system(ax, origin_world, R_world, 'W', 'b')
draw_coordinate_system(ax, origin_camera, R_camera, 'C', 'r')

# 点の定義（例として世界座標系の点をカメラ座標系に変換）
point_world = np.array([2, 2, 2])
point_camera = R_camera @ point_world + origin_camera

# 点の描画
ax.scatter(*point_world, color='b')
ax.text(*point_world, 'P_w', color='b')
ax.scatter(*point_camera, color='r')
ax.text(*point_camera, 'P_c', color='r')

# 図の設定
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Coordinate Systems: World (W) and Camera (C)')
ax.view_init(20, 30)

plt.show()
