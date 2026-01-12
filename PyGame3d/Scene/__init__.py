from abc import ABC,abstractmethod

from PyGame3d.GameObject import GameContainer,ContainerComponent
from PyGame3d.GameObject.Camera import Camera
from PyGame3d.Scene.Event import EventListener

from pygame.event import Event

# Spriteの移動など外部的な処理に使うUpdataとStart
# PyGame3d.GameObject.SimpleGameObjectと役割が明確に異なっているので注意
class GameScript (ABC) :
    @abstractmethod
    def update (self,delta_MS:float) -> None :
        return
    @abstractmethod
    def start (self) -> None :
        return
    
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
    @abstractmethod
    def get_camera (self) -> Camera :
        pass
    @abstractmethod
    def script_add (self,game_script:GameScript) -> None :
        pass
    @abstractmethod
    def get_event_listener (self) -> list[EventListener] :
        pass
class Scene (SceneComponent) :
    camera : Camera
    container : GameContainer 
    exe : list[GameScript]
    ev : list[EventListener]
    def __init__(self) -> None:
        self.container = GameContainer()
        self.camera = Camera ()
        self.exe = []
        self.ev = []
        self.start()
    def script_add(self,game_script:GameScript) -> None:
        self.exe.append(game_script)
    def start(self) :
        for e in self.exe :
            e.start()
        for c in self.container.get_child() :
            c.start()
    def get_container(self) -> ContainerComponent:
        return self.container
    def add_child(self,object:ContainerComponent) -> None :
        self.container.add_child(object)
    def update (self,delta_MS:float):
        for e in self.exe :
            e.update(delta_MS)
        for c in self.container.get_child() :
            c.update(delta_MS)
    def get_camera(self) -> Camera:
        return self.camera
    def get_event_listener(self) -> list[EventListener]:
        return self.ev
