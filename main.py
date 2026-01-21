# include<>
import PyGame3d
import math
from PyGame3d.GameObject.Cube import Cube,Floor,CuttingBoad
from PyGame3d.GameObject.sprite import Sprite3D
from PyGame3d.GameObject import CollisionManager, GameContainer
from PyGame3d.vector import Vector3

# おまじない
game = PyGame3d.Application(fps=60,check_performance=True)
game.init() 

# 変数定義
angle = 0.0
# ゲーム内オブジェクトを定義
cube = Cube()
cube.name = "move_obj"
cube.position = Vector3(0,10,0)
floor = Floor()
floor.set_position(Vector3(0,-10,0))
useTextureObj = Sprite3D.obj("./Assets/u.obj","./Assets/tex.png")
game.stage.camera.position = Vector3(0,0,10)
cutting = CuttingBoad("./Assets/tex.png")
cutting.position = Vector3(0,5,-5)
cutting.scale = Vector3(5,5,5)
# 当たり判定の設定
floor.set_collide_enabled(True)
cube.set_collide_enabled(True)
cube.set_velocity_enabled(True)
# コンテナ定義
container = GameContainer()
# コンテナに追加
container.add_children([useTextureObj,cube,floor,cutting])
# stageに追加
game.stage.add_child(container)
# update関数定義
def update (delta_MS:float) -> None :
    global angle
    angle += delta_MS * 0.001
    game.stage.camera.position = Vector3(math.sin(angle),0,math.cos(angle))*10
    game.stage.camera.look_at(Vector3(0,0,0))
# tickerに追加
func_id = game.stage.ticker_add(update)
# おまじない（while文スタート ）
game.start_rendering()
