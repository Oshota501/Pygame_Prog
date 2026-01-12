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
    def start(self) -> None:
        game.stage_add_child(self.cube)
    def update(self, delta_MS: float) -> None:
        self.cube.rotation.x += 60 * delta_MS/1000
        c = scene.get_camera()
        c.add_rotation(Vector3(0.5,0.0,0.0))

scene.script_add(GameObject())
game.start_rendering()