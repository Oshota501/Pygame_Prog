import math
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

# おまじない
game = Application()
game.init() 

# ゲームのシーン設定
class StartScene (Scene) :
    sprite : Sprite3D
    floor : Floor
    cube : Cube
    sign : CuttingBoad
    angle : float

    def __init__(self) -> None:
        super().__init__()
        self.sprite = Sprite3D.obj("./Assets/u.obj")
        self.sprite.position = Vector3(0,0,0)
        self.floor = Floor.transform(position=Vector3(0,-3,0))
        self.cube = Cube()
        self.sign = CuttingBoad("./Assets/py.png")
        container = GameContainer()
        container.add_children([self.sprite,self.floor,self.cube,self.sign])
        self.add_child(container)
        self.camera.set_position(Vector3(0,0,10))
        self.sign.position = Vector3(0,5,-10)
        self.sign.scale.x = 2.6
        self.sign.scale *= 5
        self.angle = 0
    def update(self, delta_time: float):
        super().update(delta_time)
        self.angle += delta_time
        self.camera.position = Vector3(math.sin(self.angle),0.5,math.cos(self.angle))*10
        self.camera.look_at (Vector3(0,0,0))
        
game.set_scene(StartScene())
# おまじない（while文スタート ）
game.start_rendering()