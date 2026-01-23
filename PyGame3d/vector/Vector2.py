from typing import Union
import PyGame3d.vector.vec_type as vector
import math

# signature : Claude AI
class Vector2:
	x: float
	y: float

	def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
		self.x = float(x)
		self.y = float(y)

	def __repr__(self) -> str:
		return f"Vector2({self.x}, {self.y})"

	def __iter__(self):
		yield self.x
		yield self.y

	def set(self, vec: vector.VectorLike) -> None:
		ox, oy, _ = vector.as_components(vec)
		self.x, self.y = ox, oy

	def length(self) -> float:
		return math.sqrt(self.x * self.x + self.y * self.y)

	def length_squared(self) -> float:
		return self.x * self.x + self.y * self.y

	def normalized(self) -> "Vector2":
		l = self.length()
		if l == 0.0:
			return Vector2(0.0, 0.0)
		inv = 1.0 / l
		return Vector2(self.x * inv, self.y * inv)

	def dot(self, other: vector.VectorLike) -> float:
		ox, oy, _ = vector.as_components(other)
		return self.x * ox + self.y * oy

	def to_list(self) -> list[float]:
		return [self.x, self.y]

	# glsl風のブロードキャスト演算（ベクトル/スカラー両対応）
	def __add__(self, other: Union[vector.Number, vector.VectorLike]) -> "Vector2":
		ox, oy, _ = vector.as_components(other)
		return Vector2(self.x + ox, self.y + oy)

	def __radd__(self, other: Union[vector.Number, vector.VectorLike]) -> "Vector2":
		return self.__add__(other)

	def __sub__(self, other: Union[vector.Number, vector.VectorLike]) -> "Vector2":
		ox, oy, _ = vector.as_components(other)
		return Vector2(self.x - ox, self.y - oy)

	def __rsub__(self, other: Union[vector.Number, vector.VectorLike]) -> "Vector2":
		ox, oy, _ = vector.as_components(other)
		return Vector2(ox - self.x, oy - self.y)

	def __mul__(self, other: Union[vector.Number, vector.VectorLike]) -> "Vector2":
		ox, oy, _ = vector.as_components(other)
		return Vector2(self.x * ox, self.y * oy)

	def __rmul__(self, other: Union[vector.Number, vector.VectorLike]) -> "Vector2":
		return self.__mul__(other)

	def __truediv__(self, other: Union[vector.Number, vector.VectorLike]) -> "Vector2":
		ox, oy, _ = vector.as_components(other)
		return Vector2(self.x / ox, self.y / oy)

	def __rtruediv__(self, other: Union[vector.Number, vector.VectorLike]) -> "Vector2":
		ox, oy, _ = vector.as_components(other)
		return Vector2(ox / self.x, oy / self.y)

	def __neg__(self) -> "Vector2":
		return Vector2(-self.x, -self.y)

	def __eq__(self, other: object) -> bool:
		if not isinstance(other, Vector2):
			return False
		return self.x == other.x and self.y == other.y
