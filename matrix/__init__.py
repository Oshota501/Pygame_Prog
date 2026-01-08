import math
import numpy as np
# 転置済み(Transposed)の配列定義
# 数学的な行列の「行」と「列」を入れ替えて定義しています

# 移動行列
def create_translation (x:float,y:float,z:float) -> np.ndarray:
    return np.array([
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [  x,   y,   z, 1.0],
    ], dtype='f4')

# 投資投影行列
def create_perspective(fov_degrees:float, aspect_ratio:float, near:float, far:float)-> np.ndarray:
    fov_rad = math.radians(fov_degrees)
    f = 1.0 / math.tan(fov_rad / 2.0)
    
    return np.array([
        [f / aspect_ratio,    0.0,  0.0,                                   0.0],
        [0.0,                 f,    0.0,                                   0.0],
        [0.0,                 0.0,  (far + near) / (near - far),          -1.0],
        [0.0,                 0.0,  (2.0 * far * near) / (near - far),     0.0],
    ], dtype='f4')