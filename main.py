# include<>
import PyGame3d
import math
# おまじない
game = PyGame3d.Application(fps=60)
game.init() 
camera = game.stage.get_camera()
light = game.stage.get_light()
# デバッグ用
PyGame3d.PerformanceInspectator (game)
# 変数定義
angle = 0.0
# ゲーム内オブジェクトを定義
cube = PyGame3d.Cube()
cube.name = "move_obj"
cube.position = PyGame3d.Vector3(0,10,0)
floor = PyGame3d.Floor()
floor.set_position(PyGame3d.Vector3(0,-10,0))
useTextureObj = PyGame3d.Sprite3D.obj("./Assets/Tree1.obj","./Assets/Leaves0120_35_S.png")
useTextureObj.position = PyGame3d.Vector3(0,-5,0)
game.stage.get_camera().position = PyGame3d.Vector3(0,0,10)
cutting = PyGame3d.CuttingBoad("./Assets/tex.png")
cutting.position = PyGame3d.Vector3(0,5,-5)
cutting.scale = PyGame3d.Vector3(5,5,5)
# 当たり判定の設定
floor.set_collide_enabled(True)
cube.set_collide_enabled(True)
cube.set_velocity_enabled(True)
# コンテナ定義
container = PyGame3d.GameContainer()
# コンテナに追加
container.add_children([useTextureObj,cube,floor,cutting])
# stageに追加
game.stage.add_child(container)
# update関数定
def update (delta_time:float) -> None :
    global angle
    camera.position = PyGame3d.Vector3(math.sin(angle),0,math.cos(angle))*10
    camera.look_at(PyGame3d.Vector3(0,0,0))
    angle += delta_time
# tickerに追加
func_id = game.stage.ticker_add(update)
# おまじない（while文スタート ）
game.start_rendering()
