from abc import ABC , abstractmethod
from PyGame3d.vector.Vector3 import Vector3
from PyGame3d.Draw import MeshLike,Transform
import math

# 描画など内部的な処理に使うUpdataとStart 
class SimpleGameObject (ABC) :
    @abstractmethod
    def update (self,delta_time:float) -> None :
        return
    @abstractmethod
    def start (self) -> None :
        return
# ------ ------ ------ ------ ------ ------ ------ ------ ------
# Container
# ------ ------ ------ ------ ------ ------ ------ ------ ------
# signature : Oshota
class PositionComponent (ABC) :
    # position
    @abstractmethod
    def get_position (self) -> Vector3 :
        pass
    @abstractmethod
    def set_position (self,absolute_position: Vector3) -> None :
        pass
    @abstractmethod
    def add_position (self,delta_position:Vector3) -> None :
        pass
    @abstractmethod
    def get_localposition (self) -> Vector3 :
        pass
    @abstractmethod
    def set_localposition (self ,local_position:Vector3) -> None :
        pass
class RotationComponent (ABC) :
    # rotation
    @abstractmethod
    def get_rotation (self) -> Vector3 :
        pass
    @abstractmethod
    def set_rotation (self,absolute_rotation: Vector3) -> None :
        pass
    @abstractmethod
    def add_rotation (self,delta_rotation:Vector3) -> None :
        pass
    @abstractmethod
    def get_localrotation (self) -> Vector3 :
        pass
    @abstractmethod
    def set_localrotation (self ,local_rotation:Vector3) -> None :
        pass
    @abstractmethod
    def look_at (self,target_position:Vector3) -> None :
        pass
class ScaleComponent (ABC) :
    # Scale
    @abstractmethod
    def get_scale (self) -> Vector3 :
        pass
    @abstractmethod
    def set_scale (self,absolute_position: Vector3) -> None :
        pass
    @abstractmethod
    def add_scale (self,delta_position:Vector3) -> None :
        pass
    @abstractmethod
    def get_localscale (self) -> Vector3 :
        pass
    @abstractmethod
    def set_localscale (self ,local_position:Vector3) -> None :
        pass

class ContainerComponent (
            SimpleGameObject,
            PositionComponent,
            RotationComponent,
            ScaleComponent,
            ABC
    ) :
    @abstractmethod
    def get_name (self) -> str :
        pass
    @abstractmethod
    def add_child (self,object:ContainerComponent) -> None :
        pass
    @abstractmethod
    def remove_child(self,index:int) -> None :
        pass
    @abstractmethod
    def get_child (self) -> list[ContainerComponent] :
        pass
    @abstractmethod
    def get_parent (self) -> ContainerComponent | None :
        pass


class Sprite3DComponent (ContainerComponent,ABC) :
    @abstractmethod
    def get_mesh (self) -> MeshLike|None :
        pass



# ------ ------ ------ ------ ------ ------ ------ ------ ------
# collide
# ------ ------ ------ ------ ------ ------ ------ ------ ------
# signature : Cursor AI,Oshota
# date : 2026/1/18

class BoundingShape (ABC) :
    """バウンディング形状の基底クラス（AABB、Sphere等）"""
    @abstractmethod
    def intersects_with(self, other: "BoundingShape") -> bool:
        """他の形状と衝突しているかどうかを判定する。"""
        pass

class AxisAlignedBoundingBox (BoundingShape) :
    """Axis-Aligned Bounding Box（軸並行バウンディングボックス）"""
    min_point : Vector3  # 最小点
    max_point : Vector3  # 最大点
    
    def __init__(self, min_point: Vector3, max_point: Vector3) -> None:
        self.min_point = min_point
        self.max_point = max_point
    
    def intersects_with(self, other: "BoundingShape") -> bool:
        """AABB同士の衝突判定"""
        if isinstance(other, AxisAlignedBoundingBox):
            return (self.min_point.x <= other.max_point.x and self.max_point.x >= other.min_point.x and
                    self.min_point.y <= other.max_point.y and self.max_point.y >= other.min_point.y and
                    self.min_point.z <= other.max_point.z and self.max_point.z >= other.min_point.z)
        elif isinstance(other, BoundingSphere):
            # AABBとSphereの衝突判定
            closest_x = max(self.min_point.x, min(other.center.x, self.max_point.x))
            closest_y = max(self.min_point.y, min(other.center.y, self.max_point.y))
            closest_z = max(self.min_point.z, min(other.center.z, self.max_point.z))
            closest_point = Vector3(closest_x, closest_y, closest_z)
            distance_squared = (other.center - closest_point).length_squared()
            return distance_squared <= other.radius * other.radius
        return False

class BoundingSphere (BoundingShape) :
    """バウンディング球体"""
    center : Vector3  # 中心点
    radius : float    # 半径
    
    def __init__(self, center: Vector3, radius: float) -> None:
        self.center = center
        self.radius = radius
    
    def intersects_with(self, other: "BoundingShape") -> bool:
        """Sphere同士、またはSphereとAABBの衝突判定"""
        if isinstance(other, BoundingSphere):
            distance = (self.center - other.center).length()
            return distance <= (self.radius + other.radius)
        elif isinstance(other, AxisAlignedBoundingBox):
            # AABBとSphereの衝突判定（AABB側の実装を利用）
            return other.intersects_with(self)
        return False

class BoundingObject (ABC) :
    """バウンディング形状を表す基底クラス。衝突検出に使用される。"""
    @abstractmethod
    def bounding (self) -> BoundingShape :
        """バウンディング形状を返す。"""
        pass
    
    def intersects(self, other: "BoundingObject") -> bool:
        """他のバウンディングオブジェクトと衝突しているかどうかを判定する。"""
        return self.bounding().intersects_with(other.bounding())

class SimpleBoundingObject(BoundingObject):
    """BoundingShapeを直接保持するBoundingObjectの実装"""
    _shape: BoundingShape
    _position: "Vector3 | None"
    _scale: "Vector3 | None"
    
    def __init__(self, shape: BoundingShape, position: "Vector3 | None" = None, scale: "Vector3 | None" = None) -> None:
        self._shape = shape
        self._position = position
        self._scale = scale
    
    def set_position(self, position: "Vector3") -> None:
        """位置を設定する"""
        self._position = position
    
    def set_scale(self, scale: "Vector3") -> None:
        """スケールを設定する"""
        self._scale = scale
    
    def bounding(self) -> BoundingShape:
        # 位置とスケールを考慮したAABBを返す
        if isinstance(self._shape, AxisAlignedBoundingBox):
            if self._position is not None or self._scale is not None:
                # 元のAABBの中心とサイズを計算
                center = Vector3(
                    (self._shape.min_point.x + self._shape.max_point.x) / 2.0,
                    (self._shape.min_point.y + self._shape.max_point.y) / 2.0,
                    (self._shape.min_point.z + self._shape.max_point.z) / 2.0
                )
                size = Vector3(
                    self._shape.max_point.x - self._shape.min_point.x,
                    self._shape.max_point.y - self._shape.min_point.y,
                    self._shape.max_point.z - self._shape.min_point.z
                )
                
                # 位置とスケールを適用
                if self._scale is not None:
                    size = Vector3(size.x * self._scale.x, size.y * self._scale.y, size.z * self._scale.z)
                
                if self._position is not None:
                    center = center + self._position
                
                half_size = Vector3(size.x / 2.0, size.y / 2.0, size.z / 2.0)
                return AxisAlignedBoundingBox(center - half_size, center + half_size)
        
        return self._shape

# シングルトンクラス
class CollisionManager:
    """衝突検出を管理するシングルトンクラス"""
    _instance: CollisionManager | None = None
    collisions: list["CollisionDetectionContainer"]
    
    def __new__(cls) -> "CollisionManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.collisions = []
        return cls._instance
    
    def register(self, obj: "CollisionDetectionContainer") -> None:
        """衝突検出対象を登録する"""
        # print ( "登録")
        if obj not in self.collisions:
            self.collisions.append(obj)
    
    def unregister(self, obj: "CollisionDetectionContainer") -> None:
        """衝突検出対象を登録解除する"""
        if obj in self.collisions:
            self.collisions.remove(obj)
    
    def check_all_collisions(self) -> None:
        """登録されている全オブジェクト間の衝突をチェックし、衝突しているペアのリストを返す"""
        n = len(self.collisions)
        
        for i in range(n):
            obj1 = self.collisions[i]
            if not obj1.is_collide_valid():
                continue
            
            for j in range(i + 1, n):
                obj2 = self.collisions[j]
                if not obj2.is_collide_valid():
                    continue
                # 衝突判定
                if obj1.check_collision_with(obj2):
                    obj1.collide(obj2)
                    obj2.collide(obj1)
        
        return 

class CollisionDetectionContainer (ContainerComponent,ABC):
    """衝突検出コンテナ。シングルトンのCollisionManagerに自動登録される"""
    _collision_manager: CollisionManager
    
    def __init__(self) -> None:
        """コンストラクタでCollisionManagerに登録"""
        super().__init__()
        self._collision_manager = CollisionManager()
        self._collision_manager.register(self)
    
    def __del__(self) -> None:
        """デストラクタでCollisionManagerから登録解除"""
        if hasattr(self, '_collision_manager'):
            self._collision_manager.unregister(self)
    
    @abstractmethod
    def is_collide_valid (self) -> bool :
        # 衝突判定が有効かどうか
        pass
    @abstractmethod
    def get_bounding_obj (self) -> list[BoundingObject] :
        """このコンテナが持つバウンディングオブジェクトのリストを返す。"""
        pass
    @abstractmethod
    def set_bounding_obj (self,obj:BoundingObject) -> None :
        pass

    def check_collision_with(self, other: "CollisionDetectionContainer") -> bool:
        """他のCollisionDetectionContainerとの衝突を判定する。"""
        if not self.is_collide_valid() or not other.is_collide_valid():
            return False
        
        self_bounds = self.get_bounding_obj()
        other_bounds = other.get_bounding_obj()
        
        # 各バウンディングオブジェクトの組み合わせで衝突をチェック
        for self_bound in self_bounds:
            for other_bound in other_bounds:
                if self_bound.intersects(other_bound):
                    return True
        return False
    
    def check_collision(self) -> list["CollisionDetectionContainer"]:
        """collisionsリストにある全オブジェクトを探索し、衝突しているオブジェクトのリストを返す"""
        collided: list["CollisionDetectionContainer"] = []
        
        for other in self._collision_manager.collisions:
            if other is self:
                continue
            if self.check_collision_with(other):
                collided.append(other)
        
        return collided
    
    @abstractmethod 
    def collide (self,other:CollisionDetectionContainer) -> None :
        # 衝突後に呼び出される関数
        pass
