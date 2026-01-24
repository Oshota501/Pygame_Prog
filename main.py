# include<>
import PyGame3d
import math
from PyGame3d.GameObject.Cube import Cube,Floor,CuttingBoad
from PyGame3d.GameObject.sprite import Sprite3D
from PyGame3d.GameObject.Container import GameContainer
from PyGame3d.vector import Vector3
import performance
# おまじない
game = PyGame3d.Application(check_performance=True)
game.init() 
camera = game.stage.get_camera()
# 変数定義
angle = 0.0
# ゲーム内オブジェクトを定義
cube = Cube()
cube.name = "move_obj"
cube.position = Vector3(0,10,0)
floor = Floor()
floor.set_position(Vector3(0,-10,0))
useTextureObj = Sprite3D.obj("./Assets/a.obj","./Assets/tex.png")
game.stage.get_camera().position = Vector3(0,0,10)
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
# update関数定
def update (delta_time:float) -> None :
    global angle
    performance.update(delta_time)
    angle += delta_time
    camera.position = Vector3(math.sin(angle),0,math.cos(angle))*10
    camera.look_at(Vector3(0,0,0))
# tickerに追加
func_id = game.stage.ticker_add(update)
# おまじない（while文スタート ）
game.start_rendering()
