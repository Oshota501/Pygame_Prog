from abc import ABC,abstractmethod

class NodeComponent(ABC) :
    @abstractmethod
    def get_child (self) -> list[NodeComponent] :
        pass
    @abstractmethod
    def add_child (self,node:NodeComponent) -> bool :
        pass
    @abstractmethod
    def remove_child (self,index:int) -> bool :
        pass

class Node (NodeComponent):
    children : list[NodeComponent]

    def __init__(self) -> None:
        self.children = []
        return
    def get_child(self) -> list[NodeComponent]:
        return self.children
    def add_child(self, node: NodeComponent) -> bool:
        self.children.append(node)
        return True
    def remove_child(self, index: int) -> bool:
        if self.children[index] :
            del self.children[index]
            return True
        else :
            return False