import math
from PyGame3d.GameObject import ContainerComponent
from PyGame3d.matrix.mat4 import Matrix4
from PyGame3d.vector import Vector3
from PyGame3d import matrix
from PyGame3d.matrix import rotation as rmatrix

class GameContainer(ContainerComponent):
    position: Vector3
    rotation: Vector3
    scale: Vector3
    child: list[ContainerComponent]
    parent: ContainerComponent | None
    name: str

    def __init__(self, name="GameContainerName") -> None:
        self.position = Vector3(0, 0, 0)
        self.scale = Vector3(1, 1, 1)
        self.rotation = Vector3(0, 0, 1)
        self.child = []
        self.parent = None
        self.name = name

    # coded by gemini
    def get_local_matrix(self) -> Matrix4:
        """
        自分自身の Position, Rotation, Scale からローカル行列を作成する
        Order: Translate * Rotate * Scale (T * R * S)
        """
        pos = self.get_localposition()
        rot = self.get_localrotation()
        sca = self.get_localscale()
        # 1. 平行移動行列
        mat_t = matrix.create_translation(pos.x, pos.y, pos.z)
        
        # 2. 回転行列 (X, Y, Zの順序は実装依存ですが、rmatrix.createがオイラー角対応と仮定)
        mat_r = rmatrix.create(rot.x, rot.y, rot.z)
        
        # 3. 拡大縮小行列
        mat_s = matrix.create_scale(sca.x, sca.y, sca.z)
        
        # 行列の掛け算 T * R * S
        # ※ライブラリの仕様によりますが、通常は 左側にある変換が「後」に適用されます。
        #   「拡大してから、回転して、移動する」のが一般的なので T * R * S の順です。
        return mat_t * mat_r * mat_s

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
            return parent_world_mat * local_mat
        
        # 親がいなければ（ルートなら）、ローカル行列がそのままワールド行列
        return local_mat

    def get_name(self) -> str:
        return self.name

    def add_child(self, object: ContainerComponent) -> None:
        object.set_parent(self)
        self.child.append(object)

    def set_parent(self, parent: ContainerComponent) -> None:
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
        return

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
        dx, dy, dz = target_position - self.get_position()
        distance_xz = math.sqrt(dx**2 + dz**2)
        # 注意: 座標系によっては dy の符号を変える必要があります
        pitch = -math.degrees(math.atan2(dy, distance_xz))
        yaw = math.degrees(math.atan2(dx, -dz))
        self.set_rotation(Vector3(pitch, yaw, 0.0))

    # Scale
    def add_scale(self, delta_scale: Vector3) -> None:
        self.scale += delta_scale

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

    def get_localscale(self) -> Vector3:
        return self.scale

    def set_localscale(self, local_scale: Vector3) -> None:
        self.scale = local_scale
        return

    @staticmethod
    def include_transform(
        position=Vector3(0, 0, 0), rotation=Vector3(0, 0, 1), scale=Vector3(1, 1, 1)
    ) -> GameContainer:
        g = GameContainer()
        g.set_position(position)
        g.set_rotation(rotation)
        g.set_scale(scale)
        return g
