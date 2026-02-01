from PyGame3d.Draw import MeshLike
from PyGame3d.GameObject.StaticGameObject import StaticGameObject
from PyGame3d.GameObject.sprite import Sprite3D
from PyGame3d.Draw.vcolormesh import VColorShaderContainer, VertColorMesh
from PyGame3d.Draw.uvmesh import UV3dMeshSub
from PyGame3d.vector import Quaternion, Vector3
from PyGame3d.GameObject.Collide import AxisAlignedBoundingBox, StaticBoundingObject

# signature : oshota


class VColorFloor(Sprite3D):
    mesh: MeshLike | None

    def __init__(self) -> None:
        super().__init__()
        import PyGame3d.static as static

        if static.context is not None:
            self.mesh = VertColorMesh.get_checkerboad_mesh(
                static.context,
                VColorShaderContainer(),
                color1=(0.0, 0.5, 0.0),
                color2=(0.01, 0.01, 0.01),
            )
        else:
            raise ValueError("まだinitされていないようです")
        self.set_bounding_obj(Vector3(-20, -5, -20), Vector3(20, 0, 20))

    @staticmethod
    def transform(
        position: Vector3 | None = None,
        rotation: Quaternion | None = None,
        scale: Vector3 | None = None,
    ) -> VColorFloor:
        f = VColorFloor()
        f.set_position(position if position is not None else Vector3(0, 0, 0))
        f.set_rotation(rotation if rotation is not None else Quaternion.identity())
        f.set_scale(scale if scale is not None else Vector3(1, 1, 1))
        return f


class Floor(StaticGameObject):
    mesh: MeshLike | None

    def __init__(
        self,
        position: Vector3,
        rotation: Quaternion,
        scale: Vector3,
        color: tuple[float, float, float],
    ) -> None:
        super().__init__(
            position=position,
            rotation=rotation,
            scale=scale,
            mesh=UV3dMeshSub.floor_mesh(color=color),
            bounding_object=[
                StaticBoundingObject(
                    AxisAlignedBoundingBox(
                        min_point=Vector3(-10, -5, -10) * scale + position,
                        max_point=Vector3(10, 0, 10) * scale + position,
                    )
                )
            ],
        )

    @staticmethod
    def transform(
        position: Vector3 | None = None,
        rotation: Quaternion | None = None,
        scale: Vector3 | None = None,
        color: tuple[float, float, float] = (1, 1, 1),
    ) -> Floor:
        f = Floor(
            position=position if position is not None else Vector3(0, 0, 0),
            rotation=rotation if rotation is not None else Quaternion.identity(),
            scale=scale if scale is not None else Vector3(1, 1, 1),
            color=color,
        )

        return f


class CuttingBoad(Sprite3D):
    def __init__(self, tex_filepath: str) -> None:
        super().__init__()
        self.mesh = UV3dMeshSub.cutting_boad(tex_filepath)
        self.set_bounding_obj(Vector3(-0.5, -0.5, 0), Vector3(0.5, 0.5, 0))

    @staticmethod
    def transform(
        tex_filepath: str,
        position: Vector3 | None = None,
        rotation: Quaternion | None = None,
        scale: Vector3 | None = None,
    ) -> CuttingBoad:
        f = CuttingBoad(tex_filepath)
        f.set_position(position if position is not None else Vector3(0, 0, 0))
        f.set_rotation(rotation if rotation is not None else Quaternion.identity())
        f.set_scale(scale if scale is not None else Vector3(1, 1, 1))
        return f
