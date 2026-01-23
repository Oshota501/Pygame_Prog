# vector.pyi

class Vector3:
    # メンバ変数
    x: float
    y: float
    z: float

    # コンストラクタ
    def __init__(self, x: float, y: float, z: float) -> None: ...

    # 足し算 (+)
    def __add__(self, other: Vector3) -> Vector3: ...

    # 引き算 (-)
    def __sub__(self, other: Vector3) -> Vector3: ...

    # printしたときの表示
    def __repr__(self) -> str: ...
    