# include<>
import PyGame3d
import math
from PyGame3d import Scene
from PyGame3d.GameObject.Cube import Cube, Floor
from PyGame3d.GameObject import GameContainer
from PyGame3d.GameObject.sprite import Sprite3D
from PyGame3d.vector import Vector3

# おまじない
game = PyGame3d.Application()
game.init() 

# ゲームのシーン設定
class StartScene (Scene) :
    sprite : Sprite3D
    floor : Floor
    cube : Cube
    angle : float

    def __init__(self) -> None:
        super().__init__()
        self.sprite = Sprite3D.obj("./Assets/u.obj","./Assets/tex.png")
        self.sprite.position = Vector3(0,0,0)
        self.floor = Floor.transform(position=Vector3(0,-3,0))
        self.cube = Cube()
        container = GameContainer()
        container.add_children([self.sprite,self.floor,self.cube])
        self.add_child(container)
        self.camera.set_position(Vector3(0,0,10))
        self.angle = 0
    def update(self, delta_MS: float):
        super().update(delta_MS)
        self.angle += delta_MS*0.001
        self.camera.position = Vector3(math.sin(self.angle),0.5,math.cos(self.angle))*10
        self.camera.look_at (Vector3(0,0,0))
        
        


game.set_scene(StartScene())
# おまじない（while文スタート ）
game.start_rendering()
