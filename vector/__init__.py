from abc import ABC , abstractmethod
from typing import Iterable, Tuple, Union

from vector.Vector3 import Vector3

Number = Union[int, float]
VectorLike = Union["Vector3", Tuple[float, float, float], Iterable[float]]

def as_components(value: Union[Number, VectorLike]) -> tuple[float, float, float]:
    if isinstance(value, (int, float)):
        f = float(value)
        return (f, f, f)
    if isinstance(value, Vector3):
        return value.x, value.y, value.z
    if isinstance(value, tuple) and len(value) == 3:
        return float(value[0]), float(value[1]), float(value[2])
    try:
        it = iter(value)  # type: ignore[arg-type]
        x = float(next(it))
        y = float(next(it))
        z = float(next(it))
        return (x, y, z)
    except Exception as e:
        raise TypeError(f"Unsupported operand type: {type(value)}") from e