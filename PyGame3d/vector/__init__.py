from typing import Iterable, Tuple, Union

from PyGame3d.vector.Vector3 import Vector3

Number = Union[int, float]
VectorLike = Union["Vector3", Tuple[float, float, float], Iterable[float]]

def as_components(value: Union[Number, VectorLike]) -> tuple[float, float, float]:
    """
    入力値を (x, y, z) の3要素に正規化します。
    - スカラー: (f, f, f)
    - Vector3: そのまま (x, y, z)
    - 3要素タプル/Iterable: (x, y, z)
    - 2要素Iterable: (x, y, 0.0) として扱います（Vector2対応）
    """
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
        try:
            z = float(next(it))
        except StopIteration:
            z = 0.0
        return (x, y, z)
    except Exception as e:
        raise TypeError(f"Unsupported operand type: {type(value)}") from e