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
    coefficient : float
    def __init__(self,
            velocity:Vector3,
            mass:float,
            use_velocity:bool = False,
            coefficient:float=0.5
    ) -> None:
        super().__init__()
        self.use_velocity = use_velocity
        self.mass = mass
        self.velocity = velocity
        self.coefficient = coefficient
    @abstractmethod
    def cal_position (self,deltaMS:float,position:Vector3) -> Vector3 :
        pass


class Sprite3DSimplePhysics (
    Sprite3DPhysicsComponent
) :
    def __init__(self,
            velocity:Vector3=Vector3(0,0,0),
            mass:float=1,
            use_velocity:bool = False
    ) -> None:
        super().__init__(velocity,mass,use_velocity=use_velocity)
    def cal_position (self,deltaMS:float,position:Vector3) -> Vector3 :
        if self.use_velocity :
            deltaS = deltaMS*0.001
            position = position + self.velocity*deltaS
        return position


class Sprite3DGravityPhysics (
    Sprite3DPhysicsComponent
) :
    _delta_position : Vector3
    def __init__(self,
            velocity:Vector3=Vector3(0,0,0),
            mass:float=1,
            use_velocity:bool = False,
    ) -> None:
        super().__init__(velocity,mass,use_velocity=use_velocity)
        self._delta_position = Vector3()
    def cal_position (self,deltaMS:float,position:Vector3) -> Vector3 :
        if self.use_velocity :
            deltaS = deltaMS*0.001
            g = static.gravity_asseleration
            self.velocity += g*deltaS
            self._delta_position = self.velocity*deltaS
        else : 
            self._delta_position = Vector3(0,0,0)
            
        return self._delta_position

class PhysicsObject (ABC) :
    @abstractmethod
    def get_physics (self) -> Sprite3DPhysicsComponent :
        pass

    def set_velocity (self,v:Vector3) -> None :
        physics = self.get_physics()
        physics.velocity = v
    def set_mass (self,mass:float) -> None :
        physics = self.get_physics()
        physics.mass = mass
    def set_velocity_enabled (self,enabled:bool) -> None :
        physics = self.get_physics()
        physics.use_velocity = enabled
    def set_elastic_module (self,m:float) -> None :
        physics = self.get_physics()
        physics.elastic_module = m

# ------ ------ ------ ------ ------ ------ ------ ------ ------
# Sprite
# ------ ------ ------ ------ ------ ------ ------ ------ ------
class Sprite3D (
    GameContainer,
    Sprite3DComponent,
    CollisionDetectionContainer,
    PhysicsObject
) :
    mesh : MeshLike | None
    _collide_enabled : bool
    _bounding_obj : list[Sprite3DBoundingObject]
    physics : Sprite3DPhysicsComponent
    is_collide : bool
    _double_collide : int
    
    def __init__(self,
            name="Sprite",
            collision:bool=False,
            mesh:MeshLike|None=None,
            bounding:list[Sprite3DBoundingObject]=[],
            physics:Sprite3DPhysicsComponent|None=None,
    ) -> None:
        # GameContainerの__init__を呼ぶ（位置やスケールの初期化）
        GameContainer.__init__(self, name)
        # CollisionDetectionContainerの__init__を明示的に呼ぶ（CollisionManagerへの登録）
        CollisionDetectionContainer.__init__(self)
        self.mesh = mesh
        self._collide_enabled = collision
        self._bounding_obj = bounding
        self.is_collide = False
        self._double_collide = 0
        # デフォルト引数の問題を回避：Noneの場合は新しいインスタンスを作成
        if physics is None:
            self.physics = Sprite3DGravityPhysics()  # デフォルトは物理演算なし
        else:
            self.physics = physics
    # @override
    def update(self,delta_MS:float):
        super().update(delta_MS)
        # 物理演算で位置を更新
        if self.is_collide :
            self._double_collide += 1
        else : 
            self._double_collide = 0 
        if self.physics is not None and self._double_collide <= 3:
            self.position += self.physics.cal_position(delta_MS, self.position)
        if self.mesh is not None :
            self.mesh.render(Transform(
                self.get_position(),
                self.get_rotation(),
                self.get_scale()
            ))
        self.is_collide = False
        # else :
        #     print("not set mesh")
    def get_mesh(self) -> MeshLike|None:
        return self.mesh 
    def set_transform (self,
            position : Vector3 | None = None,
            rotation : Vector3 | None = None,
            scale : Vector3 | None = None,
            velocity : Vector3 | None = None,
            mass : float | None = None,
            is_collide : bool | None = None,
            use_velocity : bool | None = None
    ) -> None :
        if position is not None :
            self.set_position (position)
        if rotation is not None :
            self.set_rotation (rotation)
        if scale is not None :
            self.set_scale (scale)
        if velocity is not None :
            self.set_velocity (velocity)
        if mass is not None :
            self.set_mass (mass)
        if is_collide is not None :
            self.set_collide_enabled (is_collide)
        if use_velocity is not None :
            self.physics.use_velocity = use_velocity
    # physics
    def get_physics(self) -> Sprite3DPhysicsComponent:
        return self.physics
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
        self.physics.velocity *= -self.physics.coefficient
        if self.physics.velocity.normalized().length_squared() <= 0.001 :
            self.set_velocity = Vector3(0,0,0)
        self.is_collide = True
        return
    # override
    # spriteオブジェクトはset命令でvelocityをリセットする仕様にします。
    def set_position(self, absolute_position: Vector3) -> None:
        super().set_position(absolute_position)
        self.set_velocity(Vector3(0,0,0))
    
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

