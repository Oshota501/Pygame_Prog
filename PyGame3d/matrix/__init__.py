import math
# from pg3_math.matrix import Matrix4
from PyGame3d.matrix.mat4 import Matrix4
# signature : oshota , gemini ai
# 転置済み(Transposed)の配列定義
# 数学的な行列の「行」と「列」を入れ替えて定義しています
def get_i () -> Matrix4 :
    return Matrix4([
        1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0,
    ])
# 移動行列
def create_translation (x:float,y:float,z:float) -> Matrix4:
    return Matrix4([
        1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
          x,   y,   z, 1.0,
    ])

# 投資投影行列
def create_perspective(fov_degrees:float, aspect_ratio:float, near:float, far:float)-> Matrix4:
    fov_rad = math.radians(fov_degrees)
    f = 1.0 / math.tan(fov_rad / 2.0)
    
    return Matrix4([
        f / aspect_ratio,    0.0,  0.0,                                   0.0,
        0.0,                 f,    0.0,                                   0.0,
        0.0,                 0.0,  (far + near) / (near - far),          -1.0,
        0.0,                 0.0,  (2.0 * far * near) / (near - far),     0.0,
    ],)
def create_scale(x:float,y:float,z:float) -> Matrix4 :
    return Matrix4([
        x,0.0, 0.0, 0.0,
        0.0,y, 0.0, 0.0,
        0.0,0.0, z, 0.0,
        0.0,0.0, 0.0, 1.0
    ])

def create_ortho(left: float, right: float, bottom: float, top: float, near: float, far: float) -> Matrix4:
    """正射影行列を作成する"""
    rml = right - left
    tmb = top - bottom
    fmn = far - near
    
    M = Matrix4()
    M[0, 0] = 2.0 / rml
    M[1, 1] = 2.0 / tmb
    M[2, 2] = -2.0 / fmn
    
    M[3, 0] = -(right + left) / rml
    M[3, 1] = -(top + bottom) / tmb
    M[3, 2] = -(far + near) / fmn
    
    return M