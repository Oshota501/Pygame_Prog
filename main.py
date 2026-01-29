import math

from PyGame3d import (
    Application,
    Sprite3D,
    Floor,
    Cube,
    CuttingBoad,
    Scene,
    Vector3,
    Vector2,
    GameContainer,
)
from PyGame3d.GameObject.Sample.player import FPSPlayer
from PyGame3d.GameObject.ui_2d import UI_2d
from PyGame3d.performance import PerformanceInspectator

# おまじない
game = Application(fps=60)
game.init()

# ゲームのシーン設定
class StartScene (Scene) :
    floor : Floor
    ui : UI_2d
    

    def __init__(self) -> None:
        super().__init__()
        self.angle = 0
        self.gun = Sprite3D.obj("./Assets/ハンドガーん/tripo_convert_1290b53c-d12a-46fb-be73-51c7fe235250.obj")
        self.player = FPSPlayer(self.get_camera())
        self.camera.add_child(self.gun)
        self.gun.set_localposition(Vector3(-0.3,-0.3,0))

        self.add_children(
            Floor.transform(position=Vector3(0,-3,0)) ,
            self.player
        )

    def start(self):
        super().start()
        
    def update(self, delta_time: float):
        super().update(delta_time)

game.set_scene(StartScene())
PerformanceInspectator(game)
# おまじない（while文スタート ）
game.start_rendering()
