import os
from PyGame3d import static
from PyGame3d.Draw.vcolormesh import VertColorMesh
from PyGame3d.Draw.uvmesh import UVMesh,UVMaterial,UVTextureImage,load_obj
from PyGame3d.GameObject import Sprite3D


class VertexColorMesh_Sprite3D (Sprite3D) :
    def __init__(self,filename:str) -> None:
        super().__init__()
        if static.vert_color_mesh is not None and static.context is not None:
            self.mesh = VertColorMesh.road_obj(static.context,static.vert_color_mesh,filename)
        else :
            raise ValueError("まだinitされていないようです")
        
class UVColorMesh_Sprite3D (Sprite3D) :
    def __init__(self,texture_filename:str,obj_filename) -> None:
        super().__init__()
        if not os.path.exists(texture_filename):
            raise FileNotFoundError(f"Texture file not found: {texture_filename}")
        tex_wall = UVTextureImage(filepath=texture_filename)
        mat_wall = UVMaterial()
        mat_wall.add_texture(tex_wall,0)
        if not os.path.exists(obj_filename):
            raise FileNotFoundError(f"Object file not found: {obj_filename}")
        self.mesh = UVMesh.load_obj(mat_wall,obj_filename=obj_filename)
