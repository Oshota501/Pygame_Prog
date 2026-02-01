"""
# StaticGameObject
Collisionの計算量を減らすためのオブジェクト
- 移動不可
- 変形不可
"""

from PyGame3d.Draw.texture import UVTexture
from PyGame3d.Draw.uvmesh import UV3dMeshSub
from PyGame3d.vector import Quaternion, Vector3
from PyGame3d.Draw import MeshLike
from PyGame3d.GameObject import DrawableContainerComponent
from PyGame3d.GameObject.Collide import (
    AxisAlignedBoundingBox,
    BoundingObject,
    CollisionDetectionContainer,
    StaticBoundingObject,
    BoundingSphere,
)
from PyGame3d.GameObject.Container import GameContainer


class StaticGameObject(
    GameContainer,
    DrawableContainerComponent,
    CollisionDetectionContainer,
):
    """
    ### Static Game Container
    このオブジェクト以降のupdateは実行されません。
    transformの変更はできません。
    """

    mesh: MeshLike | None
    _collide_enabled: bool
    _bounding_obj: list[BoundingObject]
    is_collide: bool
    _double_collide: int
    _start_frag: bool

    def __init__(
        self,
        name="Static GameObject",
        mesh: MeshLike | None = None,
        position: Vector3 | None = None,
        rotation: Quaternion | None = None,
        scale: Vector3 | None = None,
        collide_enabled: bool = True,
        bounding_object: list[BoundingObject] | None = None,
    ) -> None:
        GameContainer.__init__(self, name)
        CollisionDetectionContainer.__init__(self, is_static=True)
        # collisionsに登録されてしまうため、ここで解除する
        # すまぬ
        # なぜ登録されるかはよくわからん
        self._collision_manager.unregister(self)

        self.mesh = mesh
        self.position = position if position is not None else Vector3(0, 0, 0)
        self.rotation = rotation if rotation is not None else Quaternion.identity()
        self.scale = scale if scale is not None else Vector3(1, 1, 1)

        self._start_frag = True
        self._double_collide = 0
        self.is_collide = False
        self._collide_enabled = collide_enabled
        self._bounding_obj = bounding_object if bounding_object is not None else []

    # override
    def reset(self) -> None:
        self._collision_manager.static_unregister(self)
        return super().reset()

    def draw_update(self) -> None:
        if self.mesh is not None:
            self.mesh.render(self.get_world_matrix())
        super().draw_update()

    def update(self, delta_time: float):
        return

    # implements
    def is_collide_valid(self) -> bool:
        return self._collide_enabled

    def get_bounding_obj(self) -> list[BoundingObject]:
        return self._bounding_obj

    def collide(self, other: CollisionDetectionContainer) -> None:
        return

    def set_bounding_obj(self, obj: BoundingObject) -> None:
        self._bounding_obj = [obj]
        return

    def get_mesh(self) -> MeshLike | None:
        return self.mesh

    def __repr__(self) -> str:
        result = super().__repr__()
        result += f"infomation : This object is Immutable\n"
        return result

    def load_obj(self, file_path: str) -> None:
        from PyGame3d.Draw.uvmesh import UV3dMesh
        import os

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Object file not found: {file_path}")
        self.mesh = UV3dMesh.load_obj(file_path)

    @staticmethod
    def cube(
        color: tuple[float, float, float, float] = (1, 1, 1, 1),
        position: Vector3 | None = None,
        rotation: Quaternion | None = None,
        scale: Vector3 | None = None,
    ) -> StaticGameObject:
        scale_v = scale if scale is not None else Vector3(1, 1, 1)
        position_v = position if position is not None else Vector3(0, 0, 0)
        result = StaticGameObject(
            mesh=UV3dMeshSub.get_cube_data(UVTexture.color(color)),
            position=position,
            rotation=rotation,
            scale=scale,
            bounding_object=[
                StaticBoundingObject(
                    AxisAlignedBoundingBox(
                        min_point=-scale_v * 0.5 + position_v,
                        max_point=scale_v * 0.5 + position_v,
                    )
                )
            ],
        )
        return result

    @staticmethod
    def get_bounging_AABB_edge(
        min_point: Vector3, max_point: Vector3
    ) -> StaticBoundingObject:
        return StaticBoundingObject(
            AxisAlignedBoundingBox(min_point=min_point, max_point=max_point)
        )

    @staticmethod
    def get_bounging_Sphere(center: Vector3, radius: float) -> StaticBoundingObject:
        return StaticBoundingObject(BoundingSphere(center=center, radius=radius))

    @staticmethod
    def get_bounding_AABB_core(center: Vector3, scale: Vector3) -> StaticBoundingObject:
        return StaticBoundingObject(
            AxisAlignedBoundingBox(center - scale * 0.5, center + scale * 0.5)
        )

    @staticmethod
    def obj(
        obj_filename: str,
        position: Vector3 | None = None,
        rotation: Quaternion | None = None,
        scale: Vector3 | None = None,
        bounding_obj: list[BoundingObject] = [],
    ) -> StaticGameObject:
        from PyGame3d.Draw.uvmesh import UV3dMesh
        import os

        if not os.path.exists(obj_filename):
            raise FileNotFoundError(f"Object file not found: {obj_filename}")

        return StaticGameObject(
            position=position,
            rotation=rotation,
            scale=scale,
            bounding_object=bounding_obj,
            mesh=UV3dMesh.load_obj(filename=obj_filename),
        )
