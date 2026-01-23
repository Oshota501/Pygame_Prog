from abc import ABC,abstractmethod
from typing import Callable, Mapping

from PyGame3d.GameObject import ContainerComponent
from PyGame3d.GameObject.Camera import Camera
from PyGame3d.GameObject.Collide import CollisionManager
from PyGame3d.GameObject.Container import GameContainer
from PyGame3d.Scene.Event import EventListener

from pygame.event import Event

# signature : oshota
# Spriteの移動など外部的な処理に使うUpdataとStart
# PyGame3d.GameObject.SimpleGameObjectと役割が明確に異なっているので注意
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
    def get_event_listener (self) -> list[EventListener] :
        pass
class Scene (SceneComponent) :
    camera : Camera
    exe : list[GameScript]
    ev : list[EventListener]
    ticker : dict[int,Callable[[float],None]]
    _interval_id_top : int
    _manager : CollisionManager
    def __init__(self) -> None:
        super().__init__()
        self.camera = Camera ()
        self.exe = []
        self.ev = []
        self.ticker = {}
        self.start()
        self._interval_id_top = 0 
        self._manager = CollisionManager()
    def script_add(self,game_script:GameScript) -> None:
        self.exe.append(game_script)
    def start(self) :
        for e in self.exe :
            e.start()
        for c in self.container.get_child() :
            c.start()
    def update (self,delta_time:float):
        for e in self.exe :
            e.update(delta_time)
        for c in self.container.get_child() :
            c.update(delta_time)
        for t in self.ticker.items() :
            t[1](delta_time)
        # CollideManager
        self._manager.check_all_collisions()
    def get_camera(self) -> Camera:
        return self.camera
    def get_event_listener(self) -> list[EventListener]:
        return self.ev
    def ticker_add(self, func: Callable[[float], None]) -> int:
        self.ticker[self._interval_id_top] = func
        self._interval_id_top += 1
        return self._interval_id_top - 1 
    def ticker_remove(self, func_id: int) -> None:
        del self.ticker[func_id]
    
    @staticmethod
    def default () -> Scene :
        from PyGame3d.GameObject.Cube import Floor
        from PyGame3d.vector import Vector3
        s = Scene()
        floor = Floor.include_transform(position=Vector3(0,0,0))
        background = GameContainer()
        background.add_child(floor)
        s.camera.position = Vector3(0,1,0)
        s.add_child(background)
        return s
