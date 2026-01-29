from PyGame3d.GameObject import ContainerComponent
from PyGame3d.matrix.mat4 import Matrix4
from PyGame3d import matrix
from PyGame3d.matrix import rotation as rmatrix
from PyGame3d.vector import Vector3
import math


# signature : Oshota
class Light(ContainerComponent):
    position: Vector3
    rotation: Vector3
    child: list[ContainerComponent]
    parent: ContainerComponent | None
    color: Vector3

    def __init__(self) -> None:
        self.position = Vector3(0, 10, 0)
        self.rotation = Vector3(0, -1, 0)
        self.child = []
        self.parent = None
        self.color = Vector3(1.0, 1.0, 1.0)

    def get_color(self) -> Vector3:
        return self.color

    def get_name(self) -> str:
        return "Camera"

    def add_child(self, object: ContainerComponent) -> None:
        object.set_parent(self)
        self.child.append(object)

    def get_child(self) -> list[ContainerComponent]:
        return self.child

    def remove_child(self, index: int) -> None:
        pr_pointer = self.child[index].get_parent()
        pr_pointer = None
        del self.child[index]

    def get_parent(self) -> ContainerComponent | None:
        return self.parent

    def set_parent(self, parent: ContainerComponent) -> None:
        self.parent = parent
        return

    def start(self):
        for c in self.child:
            c.start()
        return

    def update(self, delta_time: float):
        for c in self.child:
            c.update(delta_time)
        return

    def draw_update(self) -> None:
        for c in self.child:
            c.draw_update()
        return None

    def get_local_matrix(self) -> Matrix4:
        """
        自分自身の Position, Rotation, Scale からローカル行列を作成する
        Order: Translate * Rotate * Scale (T * R * S)
        """
        pos = self.get_localposition()
        rot = self.get_localrotation()
        sca = self.get_localscale()

        mat_t = matrix.create_translation(pos.x, pos.y, pos.z)

        mat_r = rmatrix.create(rot.x, rot.y, rot.z)
        
        mat_s = matrix.create_scale(sca.x, sca.y, sca.z)

        return mat_t * mat_r * mat_s

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

    def look_at(self, target_position: Vector3) -> None:
        dl = target_position - self.position
        distance_xz = math.sqrt(dl.x**2 + dl.y**2 + dl.z**2)

        # OpenGLのカメラ行列の実装によっては、上下の回転方向が逆
        pitch = -math.degrees(math.atan2(dl.y, distance_xz))

        yaw = math.degrees(math.atan2(dl.x, -dl.z))
        self.set_rotation(Vector3(pitch, yaw, 0.0))

    # Scale
    def add_scale(self, delta_scale: Vector3) -> None:
        print("\033[33mWarning : Camera doesn't have scale .")
        return

    def get_scale(self) -> Vector3:
        print("\033[33mWarning : Camera doesn't have scale .")
        return Vector3(1.0, 1.0, 1.0)

    def set_scale(self, absolute_scale: Vector3 | int | float) -> None:
        print("\033[33mWarning : Camera doesn't have scale .")
        return

    def get_localscale(self) -> Vector3:
        print("\033[33mWarning : Camera doesn't have scale .")
        return Vector3(1.0, 1.0, 1.0)

    def set_localscale(self, local_scale: Vector3) -> None:
        print("\033[33mWarning : Camera doesn't have scale .")
        return
