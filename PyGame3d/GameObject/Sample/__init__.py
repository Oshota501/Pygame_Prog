import math
from PyGame3d.Draw import MeshLike
from PyGame3d.GameObject.Collide import AxisAlignedBoundingBox, CollisionDetectionContainer, SimpleBoundingObject
from PyGame3d.GameObject.sprite import Sprite3D, Sprite3DBoundingObject, Sprite3DPhysicsComponent
from PyGame3d.Draw.vcolormesh import VColorShaderContainer, VertColorMesh
from PyGame3d.Draw.uvmesh import UVSubMesh,UVTexture
import PyGame3d.static as static
from PyGame3d.vector import Vector2, Vector3
import pygame

# signature : oshota
class Cube (Sprite3D) :
    def __init__(self) -> None:
        super().__init__()
        
        self.mesh = UVSubMesh.get_cube_data(UVTexture.color((0.3,0.3,0.3)))

        self.set_bounding_obj(Vector3(-0.5,-0.5,-0.5),Vector3(0.5,0.5,0.5))
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
class VColorCube (Sprite3D) :
    def __init__(self) -> None:
        super().__init__()
        if  static.context is not None:
            self.mesh = VertColorMesh.get_cube_data(static.context,VColorShaderContainer())
        else :
            raise ValueError("まだinitされていないようです")
        self.set_bounding_obj(Vector3(-0.5,-0.5,-0.5),Vector3(0.5,0.5,0.5))
    @staticmethod
    def transform (
            position=Vector3(0,0,0),
            rotation=Vector3(0,0,1),
            scale=Vector3(1,1,1)
    )-> VColorCube :
        f = VColorCube()
        f.set_position(position)
        f.set_rotation(rotation)
        f.set_scale(scale)
        return f

class VColorFloor (Sprite3D) :
    mesh : MeshLike | None
    def __init__(self) -> None:
        super().__init__()
        import PyGame3d.static as static
        if static.context is not None:
            self.mesh = VertColorMesh.get_checkerboad_mesh(static.context,VColorShaderContainer(),color1=(0.0,0.5,0.0),color2=(0.01,0.01,0.01))
        else :
            raise ValueError("まだinitされていないようです")
        self.set_bounding_obj(Vector3(-20,-5,-20),Vector3(20,0,20))
    @staticmethod
    def transform (
            position=Vector3(0,0,0),
            rotation=Vector3(0,0,1),
            scale=Vector3(1,1,1)
    )-> VColorFloor :
        f = VColorFloor()
        f.set_position(position)
        f.set_rotation(rotation)
        f.set_scale(scale)
        return f
      
class Floor (Sprite3D) :
    mesh : MeshLike | None
    def __init__(self) -> None:
        super().__init__()
        import PyGame3d.static as static
        if static.context is not None:
            self.mesh = UVSubMesh.floor_mesh(color=(0.3,0.3,0.1))
        else :
            raise ValueError("Not yet excuse Application.init() . \n First line in your source code is \n```py\nimport PyGame3d as pg\ngame=pg.Application(fps=60)\ngame = pg.init()\n```")
        self.set_bounding_obj(Vector3(-10,-5,-10),Vector3(10,0,10))
    
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
        self.mesh = UVSubMesh.cutting_boad(tex_filepath)
        self.set_bounding_obj(Vector3(-0.5,-0.5,0),Vector3(0.5,0.5,0))
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
