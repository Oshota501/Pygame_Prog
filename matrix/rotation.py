import math
import numpy as np

# X軸周りの回転行列を作る関数
def create_x(degrees:float):
    rad = math.radians(degrees)
    c = math.cos(rad)
    s = math.sin(rad)
    # 4x4行列 (列優先)
    return np.array([
        [1.0, 0.0, 0.0, 0.0],
        [0.0,   c,   s, 0.0],
        [0.0,  -s,   c, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ], dtype='f4')

# Y軸周りの回転行列を作る関数
def create_y(degrees:float):
    rad = math.radians(degrees)
    c = math.cos(rad)
    s = math.sin(rad)
    return np.array([
        [  c, 0.0,  -s, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [  s, 0.0,   c, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ], dtype='f4')

# Z軸周りの回転行列を作る関数
def create_z(degrees):
    rad = math.radians(degrees)
    c = math.cos(rad)
    s = math.sin(rad)
    return np.array([
        [  c,  -s, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [  s,   c, 0.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ], dtype='f4')