from PyGame3d.GameObject import ContainerComponent
from PyGame3d.matrix.mat4 import Matrix4
from PyGame3d import matrix
from PyGame3d.vector import Quaternion, Vector3


# signature : Oshota
class Light(ContainerComponent):
    child: list[ContainerComponent]
    parent: ContainerComponent | None
    color: Vector3

    def __init__(self) -> None:
        self.child = []
        self.parent = None
        self.color = Vector3(1.0, 1.0, 1.0)
        super().__init__()

    def get_color(self) -> Vector3:
        return self.color

    def get_name(self) -> str:
        return "Light1"

    def add_child(self, object: ContainerComponent) -> None:
        object.set_parent(self)
        self.child.append(object)

    def get_child(self) -> list[ContainerComponent]:
        return self.child

    def remove_child(self, index: int) -> None:
        c = self.child[index].get_parent()
        c = None
        del self.child[index]

    def reset(self) -> None:
        self.child = []

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
        sca = self.get_localscale()

        mat_t = matrix.create_translation(pos.x, pos.y, pos.z)

        mat_r = self.rotation.to_matrix()

        mat_s = matrix.create_scale(sca.x, sca.y, sca.z)

        return mat_s * mat_r * mat_t

    def get_world_matrix(self) -> Matrix4:
        """
        親の行列を含めた最終的なワールド座標行列を再帰的に計算する
        """
        local_mat = self.get_local_matrix()

        parent = self.get_parent()
        if parent is not None:
            parent_world_mat = parent.get_world_matrix()
            return local_mat * parent_world_mat

        return local_mat

    # Position
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

    # Rotation
    def add_rotation(self, delta_rotation: Quaternion) -> None:
        self.rotation *= delta_rotation

    def get_rotation(self) -> Quaternion:
        if self.parent == None:
            return self.rotation
        return self.parent.get_rotation() * self.rotation

    def set_rotation(self, absolute_rotation: Quaternion) -> None:
        if self.parent == None:
            self.rotation = absolute_rotation
        else:
            self.rotation = self.parent.get_rotation().inverse() * absolute_rotation
        return

    def look_at(self, target: Vector3, up: Vector3 = Vector3(0, 1, 0)) -> None:
        forward = Vector3(
            target.x - self.position.x,
            target.y - self.position.y,
            target.z - self.position.z,
        )
        self.rotation = Quaternion.look_rotation(forward, up)

    # Scale
    def get_scale(self) -> Vector3:
        if self.parent == None:
            return self.scale
        return self.parent.get_scale() * self.scale

    def set_scale(self, absolute_scale: Vector3 | int | float) -> None:
        if isinstance(absolute_scale, Vector3):
            if self.parent == None:
                self.scale = absolute_scale
            else:
                self.scale = absolute_scale / self.parent.get_scale()
        else:
            self.scale *= absolute_scale
        return

    def __repr__(self) -> str:
        result = super().__repr__()
        return result
