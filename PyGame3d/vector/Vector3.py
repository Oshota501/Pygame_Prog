from typing import Union
import PyGame3d.vector.vec_type as vector
import math

# signature : Gemini AI
class Vector3():
    x: float
    y: float
    z: float

    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __repr__(self) -> str:
        return f"Vector3({self.x}, {self.y}, {self.z})"

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def set (self,vec:vector.VectorLike) -> None :
        self.x ,self.y , self.z = vector.as_components(vec)

    def length(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def length_squared(self) -> float:
        return self.x * self.x + self.y * self.y + self.z * self.z

    def normalized(self) -> "Vector3":
        l = self.length()
        if l == 0.0:
            return Vector3(0.0, 0.0, 0.0)
        inv = 1.0 / l
        return Vector3(self.x * inv, self.y * inv, self.z * inv)

    def dot(self, other: vector.VectorLike) -> float:
        ox, oy, oz = vector.as_components(other)
        return self.x * ox + self.y * oy + self.z * oz

    def cross(self, other: vector.VectorLike) -> "Vector3":
        ox, oy, oz = vector.as_components(other)
        return Vector3(
            self.y * oz - self.z * oy,
            self.z * ox - self.x * oz,
            self.x * oy - self.y * ox,
        )

    def to_list(self) -> list[float]:
        return [self.x, self.y, self.z]

    # glsl風のブロードキャスト演算（ベクトル/スカラー両対応）
    def __add__(self, other: Union[vector.Number, vector.VectorLike]) -> "Vector3":
        ox, oy, oz = vector.as_components(other)
        return Vector3(self.x + ox, self.y + oy, self.z + oz)

    def __radd__(self, other: Union[vector.Number, vector.VectorLike]) -> "Vector3":
        return self.__add__(other)

    def __sub__(self, other: Union[vector.Number, vector.VectorLike]) -> "Vector3":
        ox, oy, oz = vector.as_components(other)
        return Vector3(self.x - ox, self.y - oy, self.z - oz)

    def __rsub__(self, other: Union[vector.Number, vector.VectorLike]) -> "Vector3":
        ox, oy, oz = vector.as_components(other)
        return Vector3(ox - self.x, oy - self.y, oz - self.z)

    def __mul__(self, other: Union[vector.Number, vector.VectorLike]) -> "Vector3":
        ox, oy, oz = vector.as_components(other)
        return Vector3(self.x * ox, self.y * oy, self.z * oz)

    def __rmul__(self, other: Union[vector.Number, vector.VectorLike]) -> "Vector3":
        return self.__mul__(other)

    def __truediv__(self, other: Union[vector.Number, vector.VectorLike]) -> "Vector3":
        ox, oy, oz = vector.as_components(other)
        return Vector3(self.x / ox, self.y / oy, self.z / oz)

    def __rtruediv__(self, other: Union[vector.Number, vector.VectorLike]) -> "Vector3":
        ox, oy, oz = vector.as_components(other)
        return Vector3(ox / self.x, oy / self.y, oz / self.z)

    def __neg__(self) -> "Vector3":
        return Vector3(-self.x, -self.y, -self.z)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector3):
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z
    def __getitem__ (self,index:int) -> float :
        if index == 0 :
            return self.x
        elif index == 1 :
            return self.y
        elif index == 2 :
            return self.z
        else : 
            raise IndexError(f"index {index} is out of range")
    def __setitem__ (self,index:int,value:float) -> None :
        if index == 0 :
            self.x = value 
        elif index == 1 : 
            self.y = value
        elif index == 2 :
            self.z = value
        else :
            raise IndexError(f"index {index} is out of range")
