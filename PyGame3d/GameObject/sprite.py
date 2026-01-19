from abc import ABC, abstractmethod
from PyGame3d import static
from PyGame3d.Draw import MeshLike, TextureLike, Transform
from PyGame3d.GameObject import (
    CollisionDetectionContainer, 
    GameContainer, 
    Sprite3DComponent,
    BoundingObject,
    BoundingShape,
    AxisAlignedBoundingBox,
    BoundingSphere,
    SimpleBoundingObject
)
from PyGame3d.vector import Vector3
import math

# signature : oshota
class Sprite3DBoundingObject(BoundingObject):
    sprite: "Sprite3D"
    
    def __init__(self, sprite: "Sprite3D") -> None:
        self.sprite = sprite
    
    def bounding(self) -> BoundingShape:
        """Sprite3Dの位置とスケールからAABBを計算する。"""
        position = self.sprite.get_position()
        scale = self.sprite.get_scale()
        
        # スケールを考慮した最小点と最大点を計算
        # 簡易実装: スケールの半分を半径として使用
        half_size = Vector3(abs(scale.x) / 2.0, abs(scale.y) / 2.0, abs(scale.z) / 2.0)
        min_point = position - half_size
        max_point = position + half_size
        
        return AxisAlignedBoundingBox(min_point, max_point)

# ------ ------ ------ ------ ------ ------ ------ ------ ------
# 物理演算 phisics caluclation
# ------ ------ ------ ------ ------ ------ ------ ------ ------
class Sprite3DPhysicsComponent (ABC) :
    mass : float
    velocity : Vector3
    gravity : bool
    def __init__(self,
            velocity:Vector3,
            mass:float,
            use_gravity:bool = False
    ) -> None:
        super().__init__()
        self.gravity = use_gravity
        self.mass = mass
        self.velocity = velocity
    @abstractmethod
    def cal_position (self,deltaMS:float,position:Vector3) -> Vector3 :
        pass


class Sprite3DSimplePhysics (
    Sprite3DPhysicsComponent
) :
    def __init__(self,
            velocity:Vector3=Vector3(0,0,0),
            mass:float=1,
            use_gravity:bool = False
    ) -> None:
        super().__init__(velocity,mass,use_gravity=use_gravity)
    def cal_position (self,deltaMS:float,position:Vector3) -> Vector3 :
        if self.gravity :
            deltaS = deltaMS*0.001
            position = position + self.velocity*deltaS
        return position


class Sprite3DGravityPhysics (
    Sprite3DPhysicsComponent
) :
    def __init__(self,
            velocity:Vector3=Vector3(0,0,0),
            mass:float=1,
            use_gravity:bool = False
    ) -> None:
        super().__init__(velocity,mass,use_gravity=use_gravity)
    def cal_position (self,deltaMS:float,position:Vector3) -> Vector3 :
        if self.gravity :
            deltaS = deltaMS*0.001
            g = static.gravity_asseleration
            self.velocity += g*deltaS
            position = position + self.velocity*deltaS
        return position

# ------ ------ ------ ------ ------ ------ ------ ------ ------
# Sprite
# ------ ------ ------ ------ ------ ------ ------ ------ ------
class Sprite3D (
    GameContainer,
    Sprite3DComponent,
    CollisionDetectionContainer
) :
    mesh : MeshLike | None
    _collide_enabled : bool
    _bounding_obj : list[Sprite3DBoundingObject]
    physics : Sprite3DPhysicsComponent
    
    def __init__(self,
            name="Sprite",
            collision:bool=False,
            mesh:MeshLike|None=None,
            bounding:list[Sprite3DBoundingObject]=[],
            physics:Sprite3DPhysicsComponent|None=None
    ) -> None:
        # GameContainerの__init__を呼ぶ（位置やスケールの初期化）
        GameContainer.__init__(self, name)
        # CollisionDetectionContainerの__init__を明示的に呼ぶ（CollisionManagerへの登録）
        CollisionDetectionContainer.__init__(self)
        self.mesh = mesh
        self._collide_enabled = collision
        self._bounding_obj = bounding
        # デフォルト引数の問題を回避：Noneの場合は新しいインスタンスを作成
        if physics is None:
            self.physics = Sprite3DGravityPhysics()  # デフォルトは物理演算なし
        else:
            self.physics = physics
    # @override
    def update(self,delta_MS:float):
        super().update(delta_MS)
        # 物理演算で位置を更新
        if self.physics is not None:
            self.set_position(self.physics.cal_position(delta_MS, self.get_position()))
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
    # CollisionDetectionContainer の実装
    def is_collide_valid(self) -> bool:
        return self._collide_enabled
    
    def set_collide_enabled(self, enabled: bool) -> None:
        self._collide_enabled = enabled
    def set_bounding_obj(self, obj: BoundingObject) -> None:
        self._bounding_obj = [obj]
        
    def get_bounding_obj(self) -> list[BoundingObject]:
        # # _bounding_objが空の場合は、Sprite3DBoundingObjectを自動追加
        # if len(self._bounding_obj) == 0 and self._collide_enabled:
        #     self._bounding_obj.append(Sprite3DBoundingObject(self))
        
        # SimpleBoundingObjectの位置とスケールを更新
        position = self.get_position()
        scale = self.get_scale()
        for bound_obj in self._bounding_obj:
            if isinstance(bound_obj, SimpleBoundingObject):
                bound_obj.set_position(position)
                bound_obj.set_scale(scale)
        
        return self._bounding_obj

    def collide(self,other:CollisionDetectionContainer) -> None:
        """you can use function when collided .please over ride."""
        return
    
    
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

