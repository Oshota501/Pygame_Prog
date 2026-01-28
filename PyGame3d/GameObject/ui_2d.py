from PyGame3d.Draw import MeshLike, Transform
from PyGame3d.Draw.mesh2d import Mesh2d
from PyGame3d.GameObject import DrawableContainerComponent
from PyGame3d.GameObject.Container import GameContainer
from PyGame3d.vector import Vector2

# GameContainerを継承していますが、z軸は全く意味をなしません。
class UI_2d (GameContainer,DrawableContainerComponent) :
    mesh : Mesh2d
    resolution_pointer : tuple[int,int]
    def __init__(self,mesh:Mesh2d,resolution:tuple[int,int] ,name="ui") -> None:
        super().__init__(name)
        self.mesh = mesh
       
    def get_mesh(self) -> MeshLike | None:
        return self.mesh
    # override
    def update(self, delta_time: float):
        transform = Transform (
            self.get_position(),
            self.get_rotation(),
            self.get_scale()
        )
        self.mesh.render(transform)
        return super().update(delta_time)
    
    @staticmethod
    def color_rect (
        color:tuple[float,float,float,float],
        size:Vector2,
        resolution_pointer:tuple[int,int]
    ) -> UI_2d :
        mesh = Mesh2d.color_rect(color,size)
        return UI_2d(mesh,resolution_pointer)
    @staticmethod
    def text(
        text: str, 
        resolution_pointer:tuple[int,int] ,
        font_size: int = 24, 
        color: tuple[int, int, int] = (255, 255, 255), 
        font_path: str | None = None ,
        
    ) -> UI_2d :
        mesh = Mesh2d.text(text,font_size,color,font_path)
        return UI_2d(mesh,resolution_pointer)
