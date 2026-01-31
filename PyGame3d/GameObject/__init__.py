from abc import ABC, abstractmethod
from PyGame3d.matrix.mat4 import Matrix4
from PyGame3d.vector import Quaternion, Vector3
from PyGame3d.Draw import MeshLike


# 描画など内部的な処理に使うUpdataとStart
class SimpleGameObject(ABC):
    """
    SimpleGameObject の Docstring
    """

    @abstractmethod
    def draw_update(self) -> None:
        pass

    @abstractmethod
    def update(self, delta_time: float) -> None:
        return

    @abstractmethod
    def start(self) -> None:
        return


# ------ ------ ------ ------ ------ ------ ------ ------ ------
# Container
# ------ ------ ------ ------ ------ ------ ------ ------ ------
# signature : Oshota
class PositionComponent(ABC):
    """
    PositionComponent の Docstring
    """

    position: Vector3

    def __init__(self, position: Vector3 | None = None) -> None:
        if position is None:
            self.position = Vector3(0, 0, 0)
        else:
            self.position = position
        super().__init__()

    # position
    @abstractmethod
    def get_position(self) -> Vector3:
        pass

    @abstractmethod
    def set_position(self, absolute_position: Vector3) -> None:
        pass

    def add_position(self, delta_position: Vector3) -> None:
        self.position += delta_position

    def get_localposition(self) -> Vector3:
        return self.position

    def set_localposition(self, local_position: Vector3) -> None:
        self.position = local_position


class RotationComponent(ABC):
    """
    RotationComponent の Docstring
    """

    rotation: Quaternion

    def __init__(self, rotation: Quaternion | None = None) -> None:
        if rotation is None:
            self.rotation = Quaternion(0, 0, 0, 1)
        else:
            self.rotation = rotation
        super().__init__()

    # rotation
    @abstractmethod
    def get_rotation(self) -> Quaternion:
        pass

    @abstractmethod
    def set_rotation(self, absolute_rotation: Quaternion) -> None:
        pass

    @abstractmethod
    def add_rotation(self, delta_rotation: Quaternion) -> None:
        pass

    def get_localrotation(self) -> Quaternion:
        return self.rotation

    def set_localrotation(self, local_rotation: Quaternion) -> None:
        self.rotation = local_rotation

    @abstractmethod
    def look_at(self, target_position: Quaternion) -> None:
        pass


class ScaleComponent(ABC):
    """
    ScaleComponent の Docstring
    """

    scale: Vector3

    def __init__(self, scale: Vector3 | None = None) -> None:
        if scale is None:
            self.scale = Vector3(1, 1, 1)
        else:
            self.scale = scale
        super().__init__()

    # Scale
    @abstractmethod
    def get_scale(self) -> Vector3:
        pass

    @abstractmethod
    def set_scale(self, absolute_position: Vector3) -> None:
        pass

    def add_scale(self, delta_position: Vector3) -> None:
        self.scale += delta_position

    def get_localscale(self) -> Vector3:
        return self.scale

    def set_localscale(self, local_position: Vector3) -> None:
        self.scale = local_position


class ContainerComponent(
    SimpleGameObject, PositionComponent, RotationComponent, ScaleComponent, ABC
):
    """
    ContainerComponent の Docstring
    """

    def __init__(self, position=Vector3(0, 0, 0)) -> None:
        super().__init__(position)

    @abstractmethod
    def get_local_matrix(self) -> Matrix4:
        pass

    @abstractmethod
    def get_world_matrix(self) -> Matrix4:
        pass

    # coded by oshota
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def add_child(self, object: ContainerComponent) -> None:
        pass

    @abstractmethod
    def remove_child(self, index: int) -> None:
        pass

    @abstractmethod
    def get_child(self) -> list[ContainerComponent]:
        pass

    @abstractmethod
    def get_parent(self) -> ContainerComponent | None:
        pass

    @abstractmethod
    def set_parent(self, parent: ContainerComponent) -> None:
        pass


class DrawableContainerComponent(ContainerComponent, ABC):
    """
    DrawableContainerComponent の Docstring
    """

    @abstractmethod
    def get_mesh(self) -> MeshLike | None:
        pass
