from PyGame3d import static
from PyGame3d.Draw.vcolormesh import VertColorMesh
from PyGame3d.Draw.uvmesh import UVMesh,UVMaterial,UVTexture
from PyGame3d.GameObject import Sprite3D


class VertexColorMesh_Sprite3D (Sprite3D) :
    def __init__(self,filename:str) -> None:
        super().__init__()
        if static.vert_color_mesh is not None and static.context is not None:
            self.mesh = VertColorMesh.road_obj(static.context,static.vert_color_mesh,filename)
        else :
            raise ValueError("まだinitされていないようです")
        
class UVColorMesh_Sprite3D (Sprite3D) :
    def __init__(self,filename:str) -> None:
        super().__init__()
        tex_wall = UVTexture("assets/wall.jpg")
        mat_wall = UVMaterial()
        mat_wall.add_texture(tex_wall,0)
        self.mesh = UVMesh(mat_wall)
