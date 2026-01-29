import math
from typing import Iterable, Sequence, List, Optional, overload, Union
import numpy as np
from PyGame3d.vector import Vector3

class Matrix4:
    m: np.ndarray   

    def __init__(self, arr: Optional[Sequence[float]]=None) -> None:
        if arr is None:
            self.m = np.array([
                1.0 , 0.0 , 0.0 , 0.0 ,
                0.0 , 1.0 , 0.0 , 0.0 ,
                0.0 , 0.0 , 1.0 , 0.0 ,
                0.0 , 0.0 , 0.0 , 1.0 ,
            ], dtype="f4")  # ← dtype="f4"を追加
        else:
            if len(arr) == 16:
                self.m = np.array(arr,dtype="f4")
            else :
                raise ValueError("Array is not 4*4 Matrix")

    def set_identity(self) -> None: 
        self.m = np.array([
            1.0 , 0.0 , 0.0 , 0.0 ,
            0.0 , 1.0 , 0.0 , 0.0 ,
            0.0 , 0.0 , 1.0 , 0.0 ,
            0.0 , 0.0 , 0.0 , 1.0 ,
        ],dtype="f4")
    @overload
    def __mul__(self, other: "Matrix4") -> "Matrix4":
        pass
    @overload
    def __mul__(self, other: List[float]) -> List[float]:
        pass
    def __mul__(self, other: Union["Matrix4", List[float]]) -> Union["Matrix4", List[float]]:
        if isinstance(other, Matrix4):
            mt = Matrix4()
            # 1次元配列を4x4の2次元配列に変形して乗算
            result_2d = self.m.reshape(4, 4) @ other.m.reshape(4, 4)
            # 結果を1次元に戻す
            mt.m = result_2d.reshape(16).astype("f4")
            return mt
        else:
            return self.mul_vec4(other)
    @overload
    def __rmul__(self, other: "Matrix4") -> "Matrix4":
        pass
    @overload
    def __rmul__(self, other: List[float]) -> List[float]:
        pass
    def __rmul__(self, other) -> Matrix4|List[float]:
        return self.mul_vec4(other)

    def mul_vec4(self, seq: Iterable[float]) -> List[float]:
        vec = list(seq)
        if len(vec) != 4:
            raise ValueError("Vector must have 4 elements")
        result = [0.0] * 4
        for i in range(4):
            for j in range(4):
                result[i] += self.m[i * 4 + j] * vec[j]
        return result

    def T(self) -> "Matrix4":
        return self.transposed()

    def transposed(self) -> "Matrix4":
        result = [0.0] * 16
        for i in range(4):
            for j in range(4):
                result[j * 4 + i] = self.m[i * 4 + j]
        return Matrix4(result)

    def __repr__(self) -> str: 
        res = "Matrix4 (\n"
        for i,m in enumerate (self.m) :
            res += str(m) + " " 
            if i % 4 == 3 :
                res += "\n"
        return res
    def to_array(self) -> List[float]: 
        return [v for v in self.m]
    def __eq__ (self, other: object) -> bool : 
        if isinstance(other,Matrix4) :
            for i,v in enumerate(other.m ):
                if not (v == self.m[i]) :
                    return False
            return True
        else :
            return False
        
    def get_item (self,line_index:int,column_index:int) -> float : 
        return self.m[line_index*4+column_index]
    def tobytes (self) -> bytes : 
        return self.m.astype("f4").tobytes()
    @overload
    def __getitem__ (self,index:int) -> float : 
        pass
    @overload
    def __getitem__(self,index:tuple[int,int]) -> float : 
        pass
    def __getitem__(self, index:int|tuple[int,int]) -> float:
        if isinstance(index,tuple) :
            return self.get_item(index[0],index[1])
        else :
            return self.m [index]

    def set_item (self,line_index:int,column_index:int,value:float) -> None : 
        if line_index*4+column_index >= 0 and line_index*4+column_index <16 :
            self.m[line_index*4+column_index] = value
        else :
            raise IndexError(f"index is out of range")
    @overload
    def __setitem__(self, index:tuple[int,int],value:float) -> None : 
        pass
    @overload
    def __setitem__(self, index:int,value:float) -> None : 
        pass
    def __setitem__(self, index:int|tuple[int,int], value:float) -> None:
        if isinstance (index,tuple) :
            self.set_item(index[0],index[1],value)
        else :
            self.m[index] = value
    
    def get_inverse(self) -> "Matrix4":
        m = self.m.reshape(4, 4)
        inv = np.linalg.inv(m)
        return Matrix4(inv.flatten())

    @staticmethod
    def identity() -> "Matrix4": 
        return Matrix4()
    @staticmethod
    def get_identity() -> "Matrix4" :
        return Matrix4()
    @staticmethod
    def from_list(arr: Sequence[float]) -> "Matrix4": 
        return Matrix4(arr)
    @staticmethod
    def get_translation (x:float,y:float,z:float) -> Matrix4:
        return Matrix4 ([
            1,0,0,0,
            0,1,0,0,
            0,0,1,0,
            x,y,z,1
        ])
    @staticmethod
    def create_perspective(fov_degrees:float, aspect_ratio:float, near:float, far:float)-> Matrix4:
        fov_rad = math.radians(fov_degrees)
        f = 1.0 / math.tan(fov_rad / 2.0)
        return Matrix4([
            f / aspect_ratio,    0.0,  0.0,                                   0.0,
            0.0,                 f,    0.0,                                   0.0,
            0.0,                 0.0,  (far + near) / (near - far),          -1.0,
            0.0,                 0.0,  (2.0 * far * near) / (near - far),     0.0,
        ])
    @staticmethod
    def create_scale(x:float,y:float,z:float) -> Matrix4 :
        return Matrix4([
            x,0.0, 0.0, 0.0,
            0.0,y, 0.0, 0.0,
            0.0,0.0, z, 0.0,
            0.0,0.0, 0.0, 1.0
        ])
    @staticmethod
    def create_euler_angles (x:float,y:float,z:float) -> Matrix4 :
        Sx, Cx = math.sin(x), math.cos(x)
        Sy, Cy = math.sin(y), math.cos(y)
        Sz, Cz = math.sin(z), math.cos(z)
        # ZYX順の回転行列
        return Matrix4([
            Cz*Cy,                  -Sz*Cx + Cz*Sy*Sx,   Sz*Sx + Cz*Sy*Cx,   0.0,
            Sz*Cy,                   Cz*Cx + Sz*Sy*Sx,  -Cz*Sx + Sz*Sy*Cx,   0.0,
           -Sy,                      Cy*Sx,              Cy*Cx,               0.0,
            0.0,                     0.0,                0.0,                 1.0
        ])

def get_translation(mat: Matrix4) -> "Vector3":
    return Vector3(mat.m[12], mat.m[13], mat.m[14])

def get_scale(mat: Matrix4) -> "Vector3":
    return Vector3(
        math.sqrt(mat.m[0]**2 + mat.m[1]**2 + mat.m[2]**2),
        math.sqrt(mat.m[4]**2 + mat.m[5]**2 + mat.m[6]**2),
        math.sqrt(mat.m[8]**2 + mat.m[9]**2 + mat.m[10]**2)
    )

def get_rotation(mat: Matrix4) -> "Vector3":
    sy = math.sqrt(mat.m[0]**2 + mat.m[4]**2)
    singular = sy < 1e-6
    if not singular:
        x = math.atan2(mat.m[9], mat.m[10])
        y = math.atan2(-mat.m[8], sy)
        z = math.atan2(mat.m[4], mat.m[0])
    else:
        x = math.atan2(-mat.m[6], mat.m[5])
        y = math.atan2(-mat.m[8], sy)
        z = 0
    return Vector3(x, y, z)

def create_translation(x: float, y: float, z: float) -> Matrix4:
    return Matrix4([
        1, 0, 0, x,
        0, 1, 0, y,
        0, 0, 1, z,
        0, 0, 0, 1
    ])
