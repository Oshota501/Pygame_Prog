from abc import ABC, abstractmethod
from typing import Callable

from PyGame3d.GameObject import ContainerComponent
from PyGame3d.GameObject.Light import Light
from PyGame3d.GameObject.Camera import Camera
from PyGame3d.GameObject.Container import GameContainer
class GameScript (ABC) :
    @abstractmethod
    def update (self,delta_time:float) -> None :
        return
    @abstractmethod
    def start (self) -> None :
        return

class SceneComponent (ABC) :
    container : GameContainer 
    def __init__(self) -> None:
        super().__init__()
        self.container = GameContainer()
    def get_container(self) -> ContainerComponent:
        return self.container
    def add_child(self,object:ContainerComponent) -> None :
        self.container.add_child(object)
    @abstractmethod
    def start (self) -> None :
        pass
    @abstractmethod
    def update (self,delta_time:float) -> None :
        pass
    @abstractmethod
    def get_camera (self) -> Camera :
        pass
    @abstractmethod
    def script_add (self,game_script:GameScript) -> None :
        pass
    @abstractmethod
    def ticker_add (self,func:Callable[[float],None]) -> int :
        pass
    @abstractmethod
    def ticker_remove (self,func_id:int) -> None :
        pass
    @abstractmethod
    def get_light (self) -> Light :
        pass