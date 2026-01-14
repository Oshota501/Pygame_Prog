from PyGame3d.Draw import MeshLike
from PyGame3d.GameObject import Sprite3D
from PyGame3d.Draw.vcolormesh import VertColorMesh
from PyGame3d.Draw.uvmesh import UVMesh
import PyGame3d.static as static
class Cube (Sprite3D) :
    def __init__(self) -> None:
        super().__init__()
        if static.vert_color_mesh is not None and static.context is not None:
            self.mesh = VertColorMesh.get_cube_data(static.context,static.vert_color_mesh)
        else :
            raise ValueError("まだinitされていないようです")
            

class Floor (Sprite3D) :
    mesh : MeshLike | None
    def __init__(self) -> None:
        super().__init__()
        import PyGame3d.static as static
        if static.vert_color_mesh is not None and static.context is not None:
            self.mesh = VertColorMesh.get_checkerboad_mesh(static.context,static.vert_color_mesh,color1=(0.0,0.5,0.0),color2=(0.01,0.01,0.01))
        else :
            raise ValueError("まだinitされていないようです")
        
class CuttingBoad (Sprite3D) :
    def __init__(self,tex_filepath:str) -> None:
        super().__init__()
        self.mesh = UVMesh.cutting_boad(tex_filepath)
