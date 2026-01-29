from abc import ABC , abstractmethod
from PyGame3d.vector import Vector3
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
    @abstractmethod
    def set_parent (self,parent:ContainerComponent) -> None :
        pass


class DrawableContainerComponent (ContainerComponent,ABC) :
    @abstractmethod
    def get_mesh (self) -> MeshLike|None :
        pass
