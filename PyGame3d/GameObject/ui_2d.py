from PyGame3d.Draw import MeshLike
from PyGame3d.Draw.mesh2d import Mesh2d
from PyGame3d.GameObject import DrawableContainerComponent
from PyGame3d.GameObject.Container import GameContainer

# GameContainerを継承していますが、z軸は全く意味をなしません。
class UI_2d (GameContainer,DrawableContainerComponent) :
    mesh : Mesh2d
    def __init__(self, name="ui") -> None:
        super().__init__(name)
       
    def get_mesh(self) -> MeshLike | None:
        return self.mesh
