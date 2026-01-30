from PyGame3d import (
    Application,
    Sprite3D,
    Floor,
    Scene,
    Vector3,
    CuttingBoad,
    Cube
)
from PyGame3d.GameObject.Sample.player import FPSPlayer
from PyGame3d.GameObject.ui_2d import UI_2d
from PyGame3d.performance import PerformanceInspectator

# おまじない
game = Application()
game.init()


# ゲームのシーン設定
class StartScene(Scene):
    floor: Floor
    ui: UI_2d

    def __init__(self) -> None:
        super().__init__()
        self.angle = 0
        self.player = FPSPlayer(self.camera)
        self.gun = Sprite3D.obj(
            "./Assets/ハンドガーん/tripo_convert_1290b53c-d12a-46fb-be73-51c7fe235250.obj"
        )
        self.cube = Cube()
        self.cube.set_collide_enabled(True)
        self.cube.set_velocity_enabled(True)
        self.cube.set_position(Vector3(0,20,0))

        self.pygamedenanishitendayo = CuttingBoad("./Assets/py.png")
        self.pygamedenanishitendayo.set_scale(Vector3(20,4,1))
        self.pygamedenanishitendayo.set_position(Vector3(0,0,-10))

        self.gun.look_at(Vector3(0,0,-1))
        self.gun.set_localposition(Vector3(0.4, -0.3, -0.9))
        
        self.camera.add_child(self.gun)

        self.add_children(Floor.transform(position=Vector3(0, -3, 0)), self.cube,self.player,self.pygamedenanishitendayo)

        self.player.set_position(Vector3(0,10,3))

    def start(self):
        super().start()

    def update(self, delta_time: float):
        super().update(delta_time)


game.set_scene(StartScene())
PerformanceInspectator(game)
# おまじない（while文スタート ）
game.start_rendering()
