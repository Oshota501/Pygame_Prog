from GameObject.GameObject import GameObjectLike
import GameObject.Node as node
from GameObject.Transform import BaseTransform,TransformLike

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
        self.Node = node.NormalListNode()
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

id_index = 1 

gameobject = BaseGameObject()