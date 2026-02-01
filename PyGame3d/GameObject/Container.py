# ------ ------ ------ ------ ------ ------ ------ ------ ------
# Container
# ------ ------ ------ ------ ------ ------ ------ ------ ------
# signature : Oshota
# date : 2026/1/31

from PyGame3d.GameObject import ContainerComponent
from PyGame3d.matrix.mat4 import Matrix4
from PyGame3d.vector import Quaternion, Vector3
from PyGame3d import matrix
import copy


class GameContainer(ContainerComponent):
    child: list[ContainerComponent]
    parent: ContainerComponent | None
    name: str
    _changed: bool

    def __init__(self, name="GameContainerName") -> None:
        self.child = []
        self.parent = None
        self.name = name
        self._changed = True
        super().__init__()

    # coded by gemini
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
        # まず自分のローカル行列を取得
        local_mat = self.get_local_matrix()

        # 親がいるなら、親のワールド行列に自分のローカル行列を掛ける
        parent = self.get_parent()
        if parent is not None:
            parent_world_mat = parent.get_world_matrix()
            # 【重要】 行列の掛け算順序: Parent * Child
            return local_mat * parent_world_mat

        # 親がいなければ（ルートなら）、ローカル行列がそのままワールド行列
        return local_mat

    def get_name(self) -> str:
        return self.name

    def add_child(self, object: ContainerComponent) -> None:
        object.set_parent(self)
        self.child.append(object)

    def set_parent(self, parent: ContainerComponent) -> None:
        self._changed = True
        self.parent = parent

    def add_children(self, children: list[ContainerComponent]) -> None:
        for child in children:
            self.add_child(child)

    def get_child(self) -> list[ContainerComponent]:
        return self.child

    def remove_child(self, index: int) -> None:
        # pr_pointer = self.child[index].get_parent()
        # pr_pointer = None
        del self.child[index]

    def reset(self) -> None:
        self.child = []

    def get_parent(self) -> ContainerComponent | None:
        return self.parent

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
        self._changed = False
        return

    def shallow_copy(self) -> GameContainer:
        return copy.copy(self)

    def deep_copy(self) -> GameContainer:
        return copy.deepcopy(self)

    # Position
    def set_localposition(self, local_position: Vector3) -> None:
        self._changed = True
        return super().set_localposition(local_position)

    def add_position(self, delta_position: Vector3) -> None:
        self._changed = True
        return super().add_position(delta_position)

    def get_position(self) -> Vector3:
        if self.parent == None:
            return self.position
        return self.parent.get_position() + self.position

    def set_position(self, absolute_position: Vector3) -> None:
        self._changed = True
        if self.parent == None:
            self.position = absolute_position
        else:
            self.position = absolute_position - self.parent.get_position()
        return

    # Rotation
    def add_rotation(self, delta_rotation: Quaternion) -> None:
        self._changed = True
        self.rotation *= delta_rotation

    def get_rotation(self) -> Quaternion:
        if self.parent == None:
            return self.rotation
        return self.parent.get_rotation() * self.rotation

    def set_localrotation(self, local_rotation: Quaternion) -> None:
        self._changed = True
        return super().set_localrotation(local_rotation)

    def set_rotation(self, absolute_rotation: Quaternion) -> None:
        self._changed = True
        if self.parent == None:
            self.rotation = absolute_rotation
        else:
            self.rotation = self.parent.get_rotation().inverse() * absolute_rotation
        return

    def look_at(self, target: Vector3, up: Vector3 = Vector3(0, 1, 0)) -> None:
        self._changed = True
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
        self._changed = True
        if isinstance(absolute_scale, Vector3):
            if self.parent == None:
                self.scale = absolute_scale
            else:
                self.scale = absolute_scale / self.parent.get_scale()
        else:
            self.scale *= absolute_scale
        return

    def set_localscale(self, local_position: Vector3) -> None:
        self._changed = True
        return super().set_localscale(local_position)

    def add_scale(self, delta_position: Vector3) -> None:
        self._changed = True
        return super().add_scale(delta_position)

    def __repr__(self) -> str:
        result = (
            f"{self.__class__.__name__} : {self.get_name()}\n"
            f"├--pos : {self.get_position()}\n"
            f"├--rot : {self.get_rotation()}\n"
            f"├--scale : {self.get_scale()}\n"
            f"├--children : {len(self.child)}\n"
        )
        repeat = min(len(self.child), 3)
        for i in range(repeat):
            result += f"   ├--{self.child[i].__class__.__name__} : {self.child[i].get_name()}\n"
        if len(self.child) > 3:
            result += "   etc ...\n"
        return result

    def __getitem__(self, index: int) -> ContainerComponent:
        if index >= 0 and index < len(self.child):
            return self.child[index]
        else:
            raise IndexError(f"Index ${index} is out of range .")

    def __setitem__(self, index: int, value: ContainerComponent):
        if index >= 0 and index < len(self.child):
            self.child[index] = value
            value.set_parent(self)
        else:
            raise IndexError(f"Index ${index} is out of range .")

    def __len__(self) -> int:
        return len(self.child)

    def __add__(self, other: ContainerComponent) -> GameContainer:
        container = self.deep_copy()
        container.child.extend(other.get_child())
        return container

    @staticmethod
    def transform(
        position: Vector3 | None = None,
        rotation: Quaternion | None = None,
        scale: Vector3 | None = None,
    ) -> GameContainer:
        g = GameContainer()
        g.set_position(position if position is not None else Vector3(0, 0, 0))
        g.set_rotation(rotation if rotation is not None else Quaternion.identity())
        g.set_scale(scale if scale is not None else Vector3(1, 1, 1))
        return g
