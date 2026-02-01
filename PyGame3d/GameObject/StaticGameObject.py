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
from PyGame3d.GameObject.Collide import AxisAlignedBoundingBox, BoundingObject, CollisionDetectionContainer, StaticBoundingObject
from PyGame3d.GameObject.Container import GameContainer


class StaticGameObject (
    GameContainer,
    DrawableContainerComponent,
    CollisionDetectionContainer,
):
    """
    ### Static Game Container
    このオブジェクト以降のupdateは実行されません。
    transformの変更はできません。
    """
    mesh : MeshLike | None
    _collide_enabled: bool
    _bounding_obj: list[BoundingObject]
    is_collide: bool
    _double_collide: int
    _start_frag: bool

    def __init__(self,
                name="Static GameObject",
                mesh:MeshLike|None = None,
                position:Vector3|None = None,
                rotation:Quaternion|None = None,
                scale:Vector3|None = None ,
                collide_enabled:bool = True ,
                bounding_object:list[BoundingObject]|None=None) -> None:
        super().__init__(name)
        CollisionDetectionContainer.__init__(self,is_static=True)
        self.mesh = mesh
        self.position = position if position is not None else Vector3(0,0,0)
        self.rotation = rotation if rotation is not None else Quaternion.identity()
        self.scale = scale if scale is not None else Vector3(1,1,1)

        self._start_frag = True
        self._double_collide = 0
        self.is_collide = False
        self._collide_enabled = collide_enabled
        self._bounding_obj = bounding_object if bounding_object is not None else []

    # override
    def start(self):
        if self.mesh is not None :
            self.mesh.render(self.get_world_matrix())
        return super().start()

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

    @staticmethod
    def cube (
            color:tuple[float,float,float,float] = (1,1,1,1),
            position:Vector3|None = None,
            rotation:Quaternion|None = None,
            scale:Vector3|None = None ) -> StaticGameObject :
        scale_v = scale if scale is not None else Vector3(1,1,1)
        result = StaticGameObject (
            mesh=UV3dMeshSub.get_cube_data(UVTexture.color(color)),
            position=position,
            rotation=rotation,
            scale=scale,
            bounding_object=[StaticBoundingObject(AxisAlignedBoundingBox(
                min_point=-scale_v*0.5,
                max_point=scale_v*0.5,
            ))]
        )
        return result
