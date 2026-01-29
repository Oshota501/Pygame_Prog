from abc import ABC,abstractmethod
from typing import Callable

from PyGame3d.Draw.shader_container import ShaderContainerComponent

from PyGame3d.GameObject.Camera import Camera
from PyGame3d.GameObject.Collide import CollisionManager
from PyGame3d.GameObject.Container import GameContainer
from PyGame3d.GameObject.Light import Light

from PyGame3d.Scene.component import GameScript, SceneComponent

# signature : oshota
# Spriteの移動など外部的な処理に使うUpdataとStart
# PyGame3d.GameObject.SimpleGameObjectと役割が明確に異なっているので注意
    
class Scene (SceneComponent) :
    camera : Camera
    exe : list[GameScript]
    ticker : dict[int,Callable[[float],None]]
    _interval_id_top : int
    _manager : CollisionManager
    shader : list[ShaderContainerComponent ]
    light : Light
    
    from PyGame3d.env import DEFAULT_SHADERS
    def __init__(self,shaders:list[ShaderContainerComponent]=DEFAULT_SHADERS) -> None:
        super().__init__()
        self.camera = Camera ()
        self.exe = []
        self.ev = []
        self.ticker = {}
        self.start()
        self._interval_id_top = 0 
        self._manager = CollisionManager()
        self.light = Light()
        self.shader = shaders
    def script_add(self,game_script:GameScript) -> None:
        self.exe.append(game_script)
    def start(self) :
        for e in self.exe :
            e.start()
        for c in self.container.get_child() :
            c.start()
    def update (self,delta_time:float):
        for shader in self.shader :
            shader.update(self)
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
    def ticker_add(self, func: Callable[[float], None]) -> int:
        self.ticker[self._interval_id_top] = func
        self._interval_id_top += 1
        return self._interval_id_top - 1 
    def ticker_remove(self, func_id: int) -> None:
        del self.ticker[func_id]
    def get_light(self) -> Light:
        return self.light 
    
    @staticmethod
    def default () -> Scene :
        from PyGame3d.GameObject.Sample import Floor
        from PyGame3d.vector import Vector3
        
        s = Scene()
        floor = Floor.include_transform(position=Vector3(0,0,0))
        background = GameContainer()
        background.add_child(floor)
        s.camera.position = Vector3(0,1,0)
        s.add_child(background)
        return s
