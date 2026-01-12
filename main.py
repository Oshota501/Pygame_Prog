import PyGame3d
from PyGame3d.GameObject.Cube import Cube
from PyGame3d.Scene import Scene,GameScript
from PyGame3d.vector import Vector3

scene = Scene()
game = PyGame3d.Application(scene)
game.init() 

class GameObject (GameScript) :
    def __init__(self) -> None:
        self.cube = Cube(game)
        self.angle = 0.0
    def start(self) -> None:
        game.stage_add_child(self.cube)
    def update(self, delta_MS: float) -> None:
        rotation = self.cube.get_rotation()
        rotation.x = self.angle
        rotation.y = self.angle
        rotation.z = self.angle
        self.angle += 0.01*delta_MS

scene.script_add(GameObject())
game.start_rendering()