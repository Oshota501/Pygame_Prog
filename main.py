import PyGame3d
from PyGame3d.GameObject.Cube import Cube

game = PyGame3d.Application()

game.init() 

class RotationCube (Cube) :
    angle : float
    def __init__(self, app: PyGame3d.Application) -> None:
        super().__init__(app)
        self.angle = 0.0
    def update(self, delta_MS: float):
        import math
        self.rotation.x = self.angle
        self.rotation.y = self.angle
        self.rotation.z = self.angle
        self.position.x = math.sin(self.angle*0.2)
        self.angle += 1
        super().update(delta_MS)

cube = RotationCube(game)
game.stage_add_child(cube)

game.start_rendering()