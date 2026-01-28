from PyGame3d import (
    Application,
    Sprite3D,
    Floor,
    Cube,
    CuttingBoad,
    Scene,
    Vector3,
    GameContainer,
)
from PyGame3d.GameObject.Sample import FPSPlayer

# おまじない
game = Application(fps=60)
game.init()

# ゲームのシーン設定
class StartScene (Scene) :
    sprite : Sprite3D
    floor : Floor
    cube : Cube
    sign : CuttingBoad
    angle : float
    player : FPSPlayer

    def __init__(self) -> None:
        super().__init__()
        self.sprite = Sprite3D.obj("./Assets/u.obj")
        self.sprite.position = Vector3(0,0,0)
        self.floor = Floor.transform(position=Vector3(0,-3,0))
        self.cube = Cube()
        self.sign = CuttingBoad("./Assets/py.png")
        self.floor.set_collide_enabled(True)
        container = GameContainer()
        # Player needs to be registered as a child so its update() runs every frame
        self.player = FPSPlayer(self.get_camera())
        container.add_children([self.sprite,self.floor,self.cube,self.sign,self.player])
        self.add_child(container)
        self.camera.set_position(Vector3(0,0,10))
        self.sign.position = Vector3(0,5,-10)
        self.sign.scale.x = 2.6
        self.sign.scale *= 5
        self.angle = 0
    def update(self, delta_time: float):
        super().update(delta_time)
        self.angle += delta_time

game.set_scene(StartScene())
# おまじない（while文スタート ）
game.start_rendering()
