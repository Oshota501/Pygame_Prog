import math
from PyGame3d.GameObject import ContainerComponent
from PyGame3d.matrix.mat4 import Matrix4
from PyGame3d.vector import Vector3
import numpy as np

from PyGame3d import matrix
from PyGame3d.matrix import rotation as rmatrix

# signature : Oshota
class Camera(ContainerComponent):
    position: Vector3
    rotation: Vector3
    child: list[ContainerComponent]
    parent: ContainerComponent | None

    def __init__(self) -> None:
        self.position = Vector3(0, 0, 0)
        self.rotation = Vector3(0, 0, 0)
        self.child = []
        self.parent = None

    def get_name(self) -> str:
        return "Camera"

    def add_child(self, object: ContainerComponent) -> None:
        object.set_parent(self)
        self.child.append(object)

    def get_child(self) -> list[ContainerComponent]:
        return self.child

    def set_parent(self, parent: ContainerComponent) -> None:
        self.parent = parent
        return

    def remove_child(self, index: int) -> None:
        pr_pointer = self.child[index].get_parent()
        pr_pointer = None
        del self.child[index]

    def get_parent(self) -> ContainerComponent | None:
        return self.parent

    def start(self):
        for c in self.child:
            c.start()
        return

    def draw_update(self) -> None:
        for c in self.child :
            c.draw_update()
        return None

    def update(self, delta_time: float):
        for c in self.child:
            c.update(delta_time)
        return

    def get_local_matrix(self) -> Matrix4:
        """
        自分自身の Position, Rotation, Scale からローカル行列を作成する
        Order: Translate * Rotate * Scale (T * R * S)
        """
        pos = self.get_localposition()
        rot = self.get_localrotation()

        mat_t = matrix.create_translation(pos.x, pos.y, pos.z)

        mat_r = rmatrix.create_camera(rot.x, rot.y, rot.z)

        return mat_t * mat_r

    def get_world_matrix(self) -> Matrix4:
        """
        親の行列を含めた最終的なワールド座標行列を再帰的に計算する
        """
        local_mat = self.get_local_matrix()
        
        parent = self.get_parent()
        if parent is not None:
            parent_world_mat = parent.get_world_matrix()
            return parent_world_mat * local_mat
        
        return local_mat
    # Position
    def add_position(self, delta_position: Vector3) -> None:
        self.position += delta_position

    def get_position(self) -> Vector3:
        if self.parent == None:
            return self.position
        return self.parent.get_position() + self.position

    def set_position(self, absolute_position: Vector3) -> None:
        if self.parent == None:
            self.position = absolute_position
        else:
            self.position = absolute_position - self.parent.get_position()
        return

    def get_localposition(self) -> Vector3:
        return self.position

    def set_localposition(self, local_position: Vector3) -> None:
        self.position = local_position
        return

    # Rotation
    def add_rotation(self, delta_rotation: Vector3) -> None:
        self.rotation += delta_rotation

    def get_rotation(self) -> Vector3:
        if self.parent == None:
            return self.rotation
        return self.parent.get_rotation() + self.rotation

    def set_rotation(self, absolute_rotation: Vector3) -> None:
        if self.parent == None:
            self.rotation = absolute_rotation
        else:
            self.rotation = absolute_rotation - self.parent.get_rotation()
        return

    def get_localrotation(self) -> Vector3:
        return self.rotation

    def set_localrotation(self, local_rotation: Vector3) -> None:
        self.rotation = local_rotation
        return

    def look_at(self, target: Vector3,up:Vector3=Vector3(0,1,0)) -> None:
        eye = np.array([self.position.x, self.position.y, self.position.z])
        tgt = np.array([target.x, target.y, target.z])

        z_axis = eye - tgt  # 手前方向 (Forwardの逆)
        z_len = np.linalg.norm(z_axis)
        if z_len < 1e-6: return # 近すぎる場合は無視
        z_axis /= z_len

        # Right (X軸): Up x Z
        up_arr = np.array([up.x, up.y, up.z])
        x_axis = np.cross(up_arr, z_axis)
        x_len = np.linalg.norm(x_axis)
        if x_len < 1e-6: x_axis = np.array([1, 0, 0]) # 万が一並行ならX軸とする
        else: x_axis /= x_len

        # Up (Y軸): Z x X
        y_axis = np.cross(z_axis, x_axis)

        pitch = math.asin(y_axis[2])  # Y軸ベクトルのZ成分がピッチに関連
        yaw = math.atan2(-z_axis[0], -z_axis[2])
        roll = 0.0

        self.rotation.x = pitch
        self.rotation.y = yaw
        self.rotation.z = roll

    # Scale
    def add_scale(self, delta_scale: Vector3) -> None:
        print("\033[33mWarning : Camera doesn't have scale .")
        return

    def get_scale(self) -> Vector3:
        return Vector3(1.0, 1.0, 1.0)

    def set_scale(self, absolute_scale: Vector3 | int | float) -> None:
        print("\033[33mWarning : Camera doesn't have scale .")
        return

    def get_localscale(self) -> Vector3:
        return Vector3(1.0, 1.0, 1.0)

    def set_localscale(self, local_scale: Vector3) -> None:
        print("\033[33mWarning : Camera doesn't have scale .")
        return
