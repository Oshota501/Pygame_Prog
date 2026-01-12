from PyGame3d.GameObject import Sprite3D
from PyGame3d.Draw.mesh import Mesh
from PyGame3d import Application

class Cube (Sprite3D) :
    def __init__(self,app:Application) -> None:
        super().__init__()
        self.mesh = Mesh.get_cube_data(app)

class Sprite3D_obj_format (Sprite3D) :
    def __init__(self,app:Application,filename:str) -> None:
        super().__init__()
        self.mesh = Mesh.road_obj(filename,app)
