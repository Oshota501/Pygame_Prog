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

class MeshLike (ABC) :
    @abstractmethod
    def render (self,transform:Transform, model_matrix=None) -> None:
        pass
    @abstractmethod
    def destroy (self) -> None:
        pass
