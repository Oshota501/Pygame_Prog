from abc import ABC, abstractmethod
from dataclasses import dataclass
import moderngl
from PyGame3d.matrix.mat4 import Matrix4
from PyGame3d.vector import Quaternion, Vector3


# signature : oshota
@dataclass
class Transform:
    position: Vector3
    rotation: Quaternion
    scale: Vector3


class MeshRender(ABC):
    """
    MeshRender の Docstring
    ContextとProgramを保持
    """

    @abstractmethod
    def get_render_obj(self) -> tuple[moderngl.Context, moderngl.Program] | None:
        pass


class TextureLike(ABC):
    """
    TextureLike の Docstring
    """

    @abstractmethod
    def get(self) -> moderngl.Texture:
        pass

    @abstractmethod
    def use(self, location: int) -> None:
        pass


class MaterialLike(ABC):
    """
    MaterialLike の Docstring
    """

    @abstractmethod
    def get_textures(self) -> dict[int, TextureLike]:
        pass

    @abstractmethod
    def use(self) -> None:
        pass

    @abstractmethod
    def add_texture(self, texture: TextureLike, location: int, uniform_name: str):
        pass


class MeshLike(ABC):
    """
    MeshLike の Docstring
    """

    @abstractmethod
    def render(self, model_matrix:Matrix4|Transform) -> None:
        pass

    @abstractmethod
    def destroy(self) -> None:
        pass

    @abstractmethod
    def get_material(self) -> MaterialLike | None:
        pass
