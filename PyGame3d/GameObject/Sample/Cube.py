from PyGame3d import static
from PyGame3d.Draw.vcolormesh import VColorShaderContainer, VertColorMesh
from PyGame3d.GameObject.Collide import AxisAlignedBoundingBox, StaticBoundingObject
from PyGame3d.GameObject.StaticGameObject import StaticGameObject
from PyGame3d.vector import Vector3
from PyGame3d.Draw.texture import UVTexture
from PyGame3d.Draw.uvmesh import UV3dMeshSub
from PyGame3d.GameObject.sprite import Sprite3D
from PyGame3d.vector import Quaternion


class Cube(Sprite3D):
    def __init__(self) -> None:
        super().__init__()

        self.mesh = UV3dMeshSub.get_cube_data(UVTexture.color((0.3, 0.3, 0.3)))

        self.set_bounding_obj(Vector3(-0.5, -0.5, -0.5), Vector3(0.5, 0.5, 0.5))

    @staticmethod
    def transform(
        position: Vector3 | None = None,
        rotation: Quaternion | None = None,
        scale: Vector3 | None = None,
    ) -> Cube:
        f = Cube()
        f.set_position(position if position is not None else Vector3(0, 0, 0))
        f.set_rotation(rotation if rotation is not None else Quaternion.identity())
        f.set_scale(scale if scale is not None else Vector3(1, 1, 1))
        return f


class VColorCube(Sprite3D):
    def __init__(self) -> None:
        super().__init__()
        if static.context is not None:
            self.mesh = VertColorMesh.get_cube_data(
                static.context, VColorShaderContainer()
            )
        else:
            raise ValueError("まだinitされていないようです")
        self.set_bounding_obj(Vector3(-0.5, -0.5, -0.5), Vector3(0.5, 0.5, 0.5))

    @staticmethod
    def transform(
        position: Vector3 | None = None,
        rotation: Quaternion | None = None,
        scale: Vector3 | None = None,
    ) -> VColorCube:
        f = VColorCube()
        f.set_position(position if position is not None else Vector3(0, 0, 0))
        f.set_rotation(rotation if rotation is not None else Quaternion.identity())
        f.set_scale(scale if scale is not None else Vector3(1, 1, 1))
        return f


class StaticCube (StaticGameObject) :
    def __init__ (self,
                position : Vector3 ,
                rotation : Quaternion ,
                scale : Vector3 ,
                color : tuple[float,float,float,float] = (1,1,1,1)
                ) -> None :
        scale_v = scale if scale is not None else Vector3(1,1,1)
        position_v = position if position is not None else Vector3 (0,0,0)
        super().__init__ (
            mesh=UV3dMeshSub.get_cube_data(UVTexture.color(color)),
            position=position,
            rotation=rotation,
            scale=scale,
            bounding_object=[StaticBoundingObject(AxisAlignedBoundingBox(
                min_point=-scale_v*0.5+position_v,
                max_point=scale_v*0.5+position_v,
            ))]
        )
