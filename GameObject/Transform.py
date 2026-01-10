from GameObject.HierarchicalVec3 import HierarchicalVector3Like,HierarchicalVector3,BaseHierarchicalVector3
from vector.Vector3 import Vector3
from abc import ABC , abstractmethod

class TransformLike(ABC) :
    @abstractmethod
    def get_position (self) -> HierarchicalVector3Like :
        pass
    @abstractmethod
    def get_rotation (self) -> HierarchicalVector3Like :
        pass
    @abstractmethod
    def get_scale (self) -> HierarchicalVector3Like :
        pass
    @abstractmethod
    def change_parent (self,parent:TransformLike) -> None :
        pass
class BaseTransform (TransformLike) :
    position : BaseHierarchicalVector3
    rotation : BaseHierarchicalVector3
    scale : BaseHierarchicalVector3

    def __init__(self) -> None:
        self.position = BaseHierarchicalVector3()
        self.rotation = BaseHierarchicalVector3()
        self.scale= BaseHierarchicalVector3()
    def change_parent (self,parent:TransformLike) -> None:
        return
    def get_position(self) -> HierarchicalVector3Like:
        return self.position
    def get_rotation(self) -> HierarchicalVector3Like:
        return self.rotation
    def get_scale(self) -> HierarchicalVector3Like:
        return self.scale
       
class Transform (TransformLike) :
    position : HierarchicalVector3
    rotation : HierarchicalVector3
    scale : HierarchicalVector3
    
    def __init__(self,parent:TransformLike,position:Vector3,rotation:Vector3,scale:Vector3) -> None:
        self.position = HierarchicalVector3(position,parent.get_position())
        self.rotation = HierarchicalVector3(rotation,parent.get_rotation())
        self.scale = HierarchicalVector3(scale,parent.get_scale())

    def change_parent (self,parent:TransformLike) -> None:
        self.position.change_parents(parent.get_position())
        self.rotation.change_parents(parent.get_rotation())
        self.scale.change_parents(parent.get_scale())

    def get_position(self) -> HierarchicalVector3Like:
        return self.position
    def get_rotation(self) -> HierarchicalVector3Like:
        return self.rotation
    def get_scale(self) -> HierarchicalVector3Like:
        return self.scale
    @staticmethod
    def encopy (transformlike:TransformLike,parent:TransformLike) -> Transform :
        return Transform(
            parent,
            transformlike.get_position().get(),
            transformlike.get_rotation().get(),
            transformlike.get_scale().get()
        )
    
    