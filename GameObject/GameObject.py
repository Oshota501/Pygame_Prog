import GameObject.Node as node
from GameObject.Transform import BaseTransform, TransformLike,Transform
from abc import ABC,abstractmethod
from Draw.mesh import MeshLike

class GameObjectLike (ABC):
    @abstractmethod
    def get_id (self) -> int :
        pass
    @abstractmethod
    def get_name (self) -> str :
        pass
    @abstractmethod
    def get_node (self) -> node.NodeComponent :
        pass
    @abstractmethod
    def get_transform (self) -> TransformLike :
        pass
    @abstractmethod 
    def add_child (self,gameobject:GameObjectLike) -> None :
        pass
    @abstractmethod
    def remove_child (self,index:int) -> bool:
        pass
    @abstractmethod
    def is_valid (self) -> bool :
        pass
    @abstractmethod
    def set_valid (self,isvalid:bool) -> bool :
        pass
    @abstractmethod
    def change_parent (self,prent:GameObjectLike) -> None :
        pass
    @abstractmethod
    def destroy (self) -> None :
        pass
    
class GameObjectMeshOption (GameObjectLike,ABC) :
    @abstractmethod
    def get_mesh (self) -> MeshLike :
        pass

# 以下また後で考える。
class GameObjectPhysicsCalculationOption (GameObjectLike,ABC) :
    @abstractmethod
    def use_gravity(self,witch:bool) -> None :
        pass
    @abstractmethod
    def use_collide(self,witch:bool) -> None :
        pass

class BaseGameObject (GameObjectLike) :
    id : int
    name : str
    valid : bool
    node : node.NormalListNode
    transform : BaseTransform

    def __init__(self) -> None:
        self.id = 0
        self.name = "base_object"
        self.valid = True
        self.node = node.NormalListNode()
        self.transform = BaseTransform()
        return
    def get_id (self) -> int :
        return self.id
    def get_name (self) -> str :
        return self.name
    def get_node (self) -> node.NodeComponent :
        return self.node
    def get_transform (self) -> TransformLike :
        return self.transform
    def add_child (self,gameobject:GameObjectLike) -> None :
        self.node.add_child(gameobject.get_node())
    def remove_child (self,index:int) -> bool:
        return self.node.remove_child(index)
    def is_valid (self) -> bool :
        return self.valid
    def set_valid (self,isvalid:bool) -> bool :
        self.valid = isvalid
        return self.valid
    def destroy(self) -> None:
        return 
    def change_parent(self, prent: GameObjectLike) -> None:
        return 

class GameObject (GameObjectLike) :
    from GameObject.Transform import Transform
    id : int
    name : str
    valid : bool
    node : node.NormalListNode
    transform : Transform

    def __init__(
                self,
                parent:GameObjectLike,
        ) -> None:
        from GameObject import id_index
        self.id = id_index
        id_index += 1
        self.name = "object"
        self.valid = True
        self.node = node.NormalListNode()
        self.transform = Transform.encopy(parent.get_transform(),parent.get_transform())
        parent.add_child(self)
        return
    def get_id (self) -> int :
        return self.id
    def get_name (self) -> str :
        return self.name
    def get_node (self) -> node.NodeComponent :
        return self.node
    def get_transform (self) -> TransformLike :
        return self.transform
    def add_child (self,gameobject:GameObjectLike) -> None :
        self.node.add_child(gameobject.get_node())
        gameobject.change_parent(self)
    def remove_child (self,index:int) -> bool:
        return self.node.remove_child(index)
    def is_valid (self) -> bool :
        return self.valid
    def set_valid (self,isvalid:bool) -> bool :
        self.valid = isvalid
        return self.valid
    def change_parent(self, parent: GameObjectLike) -> None:
        self.transform.change_parent(parent.get_transform())
        return
    def destroy(self) -> None:
        return 