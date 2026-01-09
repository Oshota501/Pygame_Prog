import vector
import math
from typing import Iterable, Tuple, Union


Number = Union[int, float]
VectorLike = Union["Vector3", Tuple[float, float, float], Iterable[float], vector.Vector3Like]


class Vector3(vector.Vector3Like):
    x: float
    y: float
    z: float

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __repr__(self) -> str:
        return f"Vector3({self.x}, {self.y}, {self.z})"

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def get_tuple(self) -> tuple[float, float, float]:
        return (self.x, self.y, self.z)

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

    def dot(self, other: VectorLike) -> float:
        ox, oy, oz = _as_components(other)
        return self.x * ox + self.y * oy + self.z * oz

    def cross(self, other: VectorLike) -> "Vector3":
        ox, oy, oz = _as_components(other)
        return Vector3(
            self.y * oz - self.z * oy,
            self.z * ox - self.x * oz,
            self.x * oy - self.y * ox,
        )

    def to_list(self) -> list[float]:
        return [self.x, self.y, self.z]

    # glsl風のブロードキャスト演算（ベクトル/スカラー両対応）
    def __add__(self, other: Union[Number, VectorLike]) -> "Vector3":
        ox, oy, oz = _as_components(other)
        return Vector3(self.x + ox, self.y + oy, self.z + oz)

    def __radd__(self, other: Union[Number, VectorLike]) -> "Vector3":
        return self.__add__(other)

    def __sub__(self, other: Union[Number, VectorLike]) -> "Vector3":
        ox, oy, oz = _as_components(other)
        return Vector3(self.x - ox, self.y - oy, self.z - oz)

    def __rsub__(self, other: Union[Number, VectorLike]) -> "Vector3":
        ox, oy, oz = _as_components(other)
        return Vector3(ox - self.x, oy - self.y, oz - self.z)

    def __mul__(self, other: Union[Number, VectorLike]) -> "Vector3":
        ox, oy, oz = _as_components(other)
        return Vector3(self.x * ox, self.y * oy, self.z * oz)

    def __rmul__(self, other: Union[Number, VectorLike]) -> "Vector3":
        return self.__mul__(other)

    def __truediv__(self, other: Union[Number, VectorLike]) -> "Vector3":
        ox, oy, oz = _as_components(other)
        return Vector3(self.x / ox, self.y / oy, self.z / oz)

    def __rtruediv__(self, other: Union[Number, VectorLike]) -> "Vector3":
        ox, oy, oz = _as_components(other)
        return Vector3(ox / self.x, oy / self.y, oz / self.z)

    def __neg__(self) -> "Vector3":
        return Vector3(-self.x, -self.y, -self.z)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector3):
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z


def _as_components(value: Union[Number, VectorLike]) -> tuple[float, float, float]:
    if isinstance(value, (int, float)):
        f = float(value)
        return (f, f, f)
    if isinstance(value, Vector3):
        return value.x, value.y, value.z
    if isinstance(value, tuple) and len(value) == 3:
        return float(value[0]), float(value[1]), float(value[2])
    if isinstance(value, vector.Vector3Like):
        x, y, z = value.get_tuple()
        return float(x), float(y), float(z)
    try:
        it = iter(value)  # type: ignore[arg-type]
        x = float(next(it))
        y = float(next(it))
        z = float(next(it))
        return (x, y, z)
    except Exception as e:
        raise TypeError(f"Unsupported operand type: {type(value)}") from e