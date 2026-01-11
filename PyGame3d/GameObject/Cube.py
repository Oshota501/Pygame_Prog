from PyGame3d.GameObject import Sprite3D
from PyGame3d.Draw.mesh import Mesh
from PyGame3d import Application

class Cube (Sprite3D) :
    def __init__(self,app:Application) -> None:
        super().__init__()
        self.mesh = Mesh.get_cube_data(app)
    def update(self, delta_MS: float):
        super().update(delta_MS)
