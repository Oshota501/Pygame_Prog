from abc import ABC,abstractmethod

from PyGame3d.GameObject import GameContainer,ContainerComponent

class SceneComponent (ABC) :
    @abstractmethod
    def get_container (self) -> ContainerComponent :
        pass
    @abstractmethod
    def add_child (self,object:ContainerComponent) -> None :
        pass
    @abstractmethod
    def start (self) -> None :
        pass
    @abstractmethod
    def update (self,delta_MS:float) -> None :
        pass

class Scene (SceneComponent) :
    container : GameContainer 
    def __init__(self) -> None:
        self.container = GameContainer()
        self.start()
    def start(self) :
        for c in self.container.get_child() :
            c.start()
    def get_container(self) -> ContainerComponent:
        return self.container
    def add_child(self,object:ContainerComponent) -> None :
        self.container.add_child(object)
    def update (self,delta_MS:float):
        for c in self.container.get_child() :
            c.update(delta_MS)

