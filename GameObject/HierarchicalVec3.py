from abc import ABC,abstractmethod
from vector.Vector3 import Vector3
from vector import VectorLike,as_components

class HierarchicalVector3Like (ABC) :
    @abstractmethod
    def set (self,position:VectorLike) -> None :
        pass
    @abstractmethod
    def get (self) -> Vector3 :
        pass
    @abstractmethod
    def set_local (self,position:VectorLike) -> None :
        pass
    @abstractmethod
    def get_local (self) -> Vector3 :
        pass
class BaseHierarchicalVector3 (HierarchicalVector3Like):
    base_vec : Vector3 
    def __init__(self) -> None :
        self.base_vec = Vector3(0,0,0)
        return
    def get(self) -> Vector3:
        return self.base_vec
    def set(self,position:VectorLike) -> None:
        self.base_vec.set(position)
        return 
    def get_local(self) -> Vector3:
        return self.base_vec
    def set_local(self,position:VectorLike) -> None:
        self.base_vec.set(position)
        return 
class HierarchicalVector3 (HierarchicalVector3Like):
    _vec : Vector3 
    _parents : HierarchicalVector3Like
    def __init__(self,vec: VectorLike,parents:HierarchicalVector3Like) -> None:
        x,y,z = as_components(vec)
        self._vec = Vector3(x,y,z)
        self._parents = parents
        return
    def set (self,v3: VectorLike) -> None :
        self._vec.set(v3)
        return
    def get (self) -> Vector3 :
        return self._vec
    def set_local (self,vec:VectorLike) -> None:
        x,y,z = as_components(vec)
        self._vec = Vector3(x,y,z) + self._parents.get()
        return
    def get_local (self) -> Vector3:
        return self._parents.get() - self._vec
    def move (self,delta:VectorLike) -> None:
        self._vec += delta
        return
    def change_parents (self,parents:HierarchicalVector3Like) -> None:
        current = self.get_local()
        self._parents = parents
        self._vec = parents.get() + current
        return 