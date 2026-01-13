from abc import ABC, abstractmethod
from dataclasses import dataclass
import moderngl
from PyGame3d.vector import Vector3

@dataclass
class Transform :
    position: Vector3
    rotation: Vector3
    scale: Vector3

class MeshRender (ABC) :
    @abstractmethod
    def get_render_obj (self) -> tuple[moderngl.Context,moderngl.Program] | None :
        pass 
class TextureLike (ABC) :
    @abstractmethod
    def get (self) -> moderngl.Texture :
        pass
    @abstractmethod
    def use(self,location:int) -> None :
        pass
class MaterialLike (ABC) :
    @abstractmethod
    def get_textures (self) -> dict[int,TextureLike] :
        pass
    @abstractmethod
    def use (self) -> None :
        pass
    @abstractmethod
    def add_texture (self,texture:TextureLike,location:int,uniform_name:str) :
        pass
class MeshLike (ABC) :
    @abstractmethod
    def render (self,transform:Transform, model_matrix=None) -> None:
        pass
    @abstractmethod
    def destroy (self) -> None:
        pass
    @abstractmethod
    def get_material (self) -> MaterialLike | None :
        pass

