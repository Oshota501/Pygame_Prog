import PyGame3d
from PyGame3d.GameObject.Cube import Cube,Sprite3D_obj_format
from PyGame3d.Scene import Scene,GameScript
from PyGame3d.vector import Vector3
import math

scene = Scene()
game = PyGame3d.Application(scene)
game.init() 

class GameObject (GameScript) :
    cube :Cube
    angle :float
    obj :Sprite3D_obj_format
    def __init__(self) -> None:
        self.cube = Cube(game)
        self.angle = 0.0
        self.obj = Sprite3D_obj_format(game,"./Assets/test.obj")
    def start(self) -> None:
        game.stage_add_child(self.cube)
        self.obj.scale *= 0.2
        game.stage_add_child(self.obj)
    def update(self, delta_MS: float) -> None:
        # rotation = self.cube.get_rotation()
        # rotation.x = self.angle
        # rotation.y = self.angle
        # rotation.z = self.angle
        game.scene.camera.position += Vector3(math.sin(self.angle),0,0)
        game.scene.camera.look_at(self.cube.get_position())
        game.scene.camera.rotation.z += 0.5
        self.angle += 0.01*delta_MS

scene.script_add(GameObject())
game.start_rendering()