"""
Quauternion
The only realize rotation .
sign : Gemini AI
"""

import math
from PyGame3d.vector import Vector3
from PyGame3d.matrix.mat4 import Matrix4


class Quaternion:
    """
    Quaternion
    to_ matrix -> Matrix4
    """

    x: float
    y: float
    z: float
    w: float

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0, w: float = 1.0):
        # w=1, xyz=0 が「無回転（Identity）」の状態です
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    @staticmethod
    def identity() -> "Quaternion":
        return Quaternion(0, 0, 0, 1)

    def conjugate(self) -> "Quaternion":
        """共役（xyzを反転、wはそのまま）を返す"""
        return Quaternion(-self.x, -self.y, -self.z, self.w)

    def inverse(self) -> "Quaternion":
        return self.conjugate()

    # --- 行列への変換 (超重要) ---

    def __repr__(self) -> str:
        return f"Quaternion({self.x},{self.y},{self.z},{self.w})"

    def to_matrix(self) -> Matrix4:
        """
        クォータニオンを回転行列(Matrix4)に変換する。
        """
        x, y, z, w = self.x, self.y, self.z, self.w

        # クォータニオンから回転行列への変換公式（列優先）
        # fmt: off
        m = Matrix4([
            1 - 2*(y*y + z*z),  2*(x*y + z*w),      2*(x*z - y*w),      0,
            2*(x*y - z*w),      1 - 2*(x*x + z*z),  2*(y*z + x*w),      0,
            2*(x*z + y*w),      2*(y*z - x*w),      1 - 2*(x*x + y*y),  0,
            0,                  0,                  0,                  1
        ])
        # fmt: on
        return m

    # --- 掛け算 (回転の合成) ---
    def __mul__(self, other: "Quaternion") -> "Quaternion":
        """
        回転A * 回転B = 回転Aのあとに回転Bを行う
        (順序はエンジンのルールによりますが、通常は右から左へ適用)
        """
        x1, y1, z1, w1 = self.x, self.y, self.z, self.w
        x2, y2, z2, w2 = other.x, other.y, other.z, other.w

        return Quaternion(
            w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
            w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
            w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
            w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
        )

    # --- LookAtの実装 (本丸) ---
    @staticmethod
    def look_rotation(forward: Vector3, up: Vector3 = Vector3(0, 1, 0)) -> "Quaternion":
        """
        UnityのQuaternion.LookRotationと同じ挙動。
        指定した方向(forward)を向くクォータニオンを作成する。
        """
        # 1. ベクトルの正規化
        # f = forward.normalized()
        f = -forward.normalized()
        u = up.normalized()

        # 2. 直交基底ベクトルを作る (LookAt行列作成と同じロジック)
        right = u.cross(f).normalized()
        new_up = f.cross(right).normalized()
        # right = f.cross(u).normalized()
        # new_up = u.cross(right).normalized()

        # 3. 回転行列の要素 (m00 ~ m22)（列優先: 列に基底を配置）
        m00, m10, m20 = right.x, new_up.x, f.x  # 第1列（right）
        m01, m11, m21 = right.y, new_up.y, f.y  # 第2列（new_up）
        m02, m12, m22 = right.z, new_up.z, f.z  # 第3列（forward）

        # 4. 行列からクォータニオンへの変換 (一番難しいところ)
        # トレース（対角成分の和）を使って分岐計算します
        trace = m00 + m11 + m22

        q = Quaternion()
        if trace > 0:
            s = 0.5 / math.sqrt(trace + 1.0)
            q.w = 0.25 / s
            q.x = (m12 - m21) * s
            q.y = (m20 - m02) * s
            q.z = (m01 - m10) * s
        else:
            if m00 > m11 and m00 > m22:
                s = 2.0 * math.sqrt(1.0 + m00 - m11 - m22)
                s_inv = 1 / s
                q.w = (m12 - m21) * s_inv
                q.x = 0.25 * s
                q.y = (m10 + m01) * s_inv
                q.z = (m20 + m02) * s_inv
            elif m11 > m22:
                s = 2.0 * math.sqrt(1.0 + m11 - m00 - m22)
                s_inv = 1 / s
                q.w = (m20 - m02) * s_inv
                q.x = (m10 + m01) * s_inv
                q.y = 0.25 * s
                q.z = (m21 + m12) * s_inv
            else:
                s = 2.0 * math.sqrt(1.0 + m22 - m00 - m11)
                s_inv = 1 / s
                q.w = (m01 - m10) * s_inv
                q.x = (m20 + m02) * s_inv
                q.y = (m21 + m12) * s_inv
                q.z = 0.25 * s

        return q

    # --- オイラー角からの変換 (互換性用) ---
    @staticmethod
    def from_euler(x: float, y: float, z: float) -> "Quaternion":
        """
        ラジアン単位のオイラー角からクォータニオンを作成
        """
        cx = math.cos(x * 0.5)
        sx = math.sin(x * 0.5)
        cy = math.cos(y * 0.5)
        sy = math.sin(y * 0.5)
        cz = math.cos(z * 0.5)
        sz = math.sin(z * 0.5)

        return Quaternion(
            sx * cy * cz - cx * sy * sz,
            cx * sy * cz + sx * cy * sz,
            cx * cy * sz - sx * sy * cz,
            cx * cy * cz + sx * sy * sz,
        )
