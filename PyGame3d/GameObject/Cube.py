from PyGame3d.Draw import MeshLike
from PyGame3d.GameObject.sprite import Sprite3D
from PyGame3d.Draw.vcolormesh import VertColorMesh
from PyGame3d.Draw.uvmesh import UVMesh
import PyGame3d.static as static
from PyGame3d.vector import Vector3

class Cube (Sprite3D) :
    def __init__(self) -> None:
        super().__init__()
        if static.vert_color_mesh is not None and static.context is not None:
            self.mesh = VertColorMesh.get_cube_data(static.context,static.vert_color_mesh)
        else :
            raise ValueError("まだinitされていないようです")
        
    @staticmethod
    def transform (
            position=Vector3(0,0,0),
            rotation=Vector3(0,0,1),
            scale=Vector3(1,1,1)
    )-> Cube :
        f = Cube()
        f.set_position(position)
        f.set_rotation(rotation)
        f.set_scale(scale)
        return f

class Floor (Sprite3D) :
    mesh : MeshLike | None
    def __init__(self) -> None:
        super().__init__()
        import PyGame3d.static as static
        if static.vert_color_mesh is not None and static.context is not None:
            self.mesh = VertColorMesh.get_checkerboad_mesh(static.context,static.vert_color_mesh,color1=(0.0,0.5,0.0),color2=(0.01,0.01,0.01))
        else :
            raise ValueError("まだinitされていないようです")
    @staticmethod
    def transform (
            position=Vector3(0,0,0),
            rotation=Vector3(0,0,1),
            scale=Vector3(1,1,1)
    )-> Floor :
        f = Floor()
        f.set_position(position)
        f.set_rotation(rotation)
        f.set_scale(scale)
        return f
        
class CuttingBoad (Sprite3D) :
    def __init__(self,tex_filepath:str) -> None:
        super().__init__()
        self.mesh = UVMesh.cutting_boad(tex_filepath)
    @staticmethod
    def transform (
            tex_filepath:str,
            position=Vector3(0,0,0),
            rotation=Vector3(0,0,1),
            scale=Vector3(1,1,1)
    )-> CuttingBoad :
        f = CuttingBoad(tex_filepath)
        f.set_position(position)
        f.set_rotation(rotation)
        f.set_scale(scale)
        return f
