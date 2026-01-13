import PyGame3d
from PyGame3d.GameObject.Cube import Cube, Floor
from PyGame3d.Scene import Scene,GameScript
from PyGame3d.vector import Vector3
import math

scene = Scene()
game = PyGame3d.Application(scene)
game.init() 

class GameObject (GameScript) :
    cube :Cube
    angle :float
    floor :Floor
    def __init__(self) -> None:
        self.cube = Cube()
        self.angle = 0.0
        self.floor = Floor()

    def start(self) -> None:
        game.stage_add_child(self.cube)
        self.floor.position.y = -3 
        game.stage_add_child(self.floor)
    def update(self, delta_MS: float) -> None :
        self.angle += 0.001*delta_MS
        self.cube.add_rotation(Vector3(math.sin(self.angle),math.cos(self.angle),math.sin(self.angle)))
        game.scene.camera.position = Vector3(math.cos(self.angle)*5,0.0,math.sin(self.angle)*5)
        game.scene.camera.look_at(self.cube.position-Vector3(0,0,0))

scene.script_add(GameObject())
game.start_rendering()