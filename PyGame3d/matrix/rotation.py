import math
import numpy as np

# signature : gemini
# X軸周りの回転行列を作る関数
def create_x(degrees:float):
    rad = math.radians(degrees)
    c = math.cos(rad)
    s = math.sin(rad)
    # 4x4行列 (列優先)
    return np.array([
        [1.0, 0.0, 0.0, 0.0],
        [0.0,   c,  -s, 0.0],
        [0.0,   s,   c, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ], dtype='f4')

# Y軸周りの回転行列を作る関数
def create_y(degrees:float):
    rad = math.radians(degrees)
    c = math.cos(rad)
    s = math.sin(rad)
    return np.array([
        [  c, 0.0,   s, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [ -s, 0.0,   c, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ], dtype='f4')

# Z軸周りの回転行列を作る関数
def create_z(degrees):
    rad = math.radians(degrees)
    c = math.cos(rad)
    s = math.sin(rad)
    return np.array([
        [  c,  -s, 0.0, 0.0],
        [  s,   c, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ], dtype='f4')

def create (x:float=0.0,y:float=0.0,z:float=0.0) -> np.ndarray:
    # X, Y, Z軸の回転を組み合わせた行列を作成
    # 回転順序: Z -> Y -> X (一般的なオイラー角の順序)
    mat_x = create_x(x)
    mat_y = create_y(y)
    mat_z = create_z(z)
    
    # 行列の積を計算 (Z * Y * X)
    return mat_x @ mat_y @ mat_z 

def create_camera (x:float=0.0,y:float=0.0,z:float=0.0) -> np.ndarray:
    # X, Y, Z軸の回転を組み合わせた行列を作成
    # 回転順序: Z -> Y -> X (一般的なオイラー角の順序)
    mat_x = create_x(x)
    mat_y = create_y(y)
    mat_z = create_z(z)
    
    # 行列の積を計算 (Z * Y * X)
    return mat_z @ mat_y @ mat_x