from PyGame3d.GameObject.Container import GameContainer
from PyGame3d.vector import Vector3
import math
# signature : Oshota
class Camera (GameContainer):
    def __init__(self) -> None:
        super().__init__("Camera")
        self.position = Vector3(0,0,3)
        self.rotation = Vector3(0,0,0)
    
    def draw_update(self) -> None:
        return None

    # Scale
    def add_scale(self, delta_scale: Vector3) -> None:
        print("\033[33mWarning : Camera doesn't have scale .")
        return
    def get_scale(self) -> Vector3:
        print("\033[33mWarning : Camera doesn't have scale .")
        return Vector3(1.0,1.0,1.0)
    def set_scale(self, absolute_scale: Vector3|int|float) -> None:
        print("\033[33mWarning : Camera doesn't have scale .")
        return
    def get_localscale(self) -> Vector3:
        print("\033[33mWarning : Camera doesn't have scale .")
        return Vector3(1.0,1.0,1.0)
    def set_localscale(self, local_scale: Vector3) -> None:
        print("\033[33mWarning : Camera doesn't have scale .")
        return
    
