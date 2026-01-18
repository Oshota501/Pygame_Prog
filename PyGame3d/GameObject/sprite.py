from PyGame3d.Draw import MeshLike, TextureLike, Transform
from PyGame3d.GameObject import GameContainer, Sprite3DComponent
from PyGame3d.vector import Vector3

# signature : oshota
class Sprite3D (
    GameContainer,
    Sprite3DComponent
) :
    mesh : MeshLike | None
    def __init__(self) -> None:
        super().__init__()
        self.mesh = None
    # @override
    def update(self,delta_MS:float):
        super().update(delta_MS)
        if self.mesh is not None :
            self.mesh.render(Transform(
                self.get_position(),
                self.get_rotation(),
                self.get_scale()
            ))
        # else :
        #     print("not set mesh")
    def get_mesh(self) -> MeshLike|None:
        return self.mesh

    # static method
    @staticmethod
    def transform (
            position=Vector3(0,0,0),
            rotation=Vector3(0,0,1),
            scale=Vector3(1,1,1)
    ) -> Sprite3D :
        g = Sprite3D()
        g.set_position(position)
        g.set_rotation(rotation)
        g.set_scale(scale)
        return g
    @staticmethod
    def obj(obj_filename:str,texture_filename:str|None=None) -> Sprite3D :
        from PyGame3d.Draw.uvmesh import UVTextureImage,UVMaterial,UVMesh,UVTexture
        import os
        result = Sprite3D()
        tex_wall : TextureLike
        if texture_filename is None :
            tex_wall = UVTexture.color((0,1,0))
        else :
            if not os.path.exists(texture_filename):
                raise FileNotFoundError(f"Texture file not found: {texture_filename}")
            tex_wall = UVTextureImage(filepath=texture_filename)
        mat_wall = UVMaterial()
        mat_wall.add_texture(tex_wall,0)
        if not os.path.exists(obj_filename):
            raise FileNotFoundError(f"Object file not found: {obj_filename}")
        result.mesh = UVMesh.load_obj(mat_wall,obj_filename=obj_filename)
        return result