import PyGame3d
import math

# おまじない
game = PyGame3d.Application(fps=64)
game.init() 
camera = game.stage.get_camera()
# デバッグ用
PyGame3d.PerformanceInspectator (game)
# 変数定義
angle = 0.0
# ゲーム内オブジェクトを定義
cube = PyGame3d.Cube()
cube.set_position(PyGame3d.Vector3(0,10,0))
floor = PyGame3d.Floor()
floor.set_position(PyGame3d.Vector3(0,-5,0))
floor.set_scale(PyGame3d.Vector3(4,4,4))
useTextureObj = PyGame3d.Sprite3D("./Assets/test.obj")
camera.set_position(PyGame3d.Vector3(0,0,10))
cutting = PyGame3d.CuttingBoad("./Assets/py.png")
cutting.position = PyGame3d.Vector3(0,5,-5)
cutting.scale = PyGame3d.Vector3(10,5,5)
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
    
    angle += delta_time
    camera.set_position(PyGame3d.Vector3(math.sin(angle),0,math.cos(angle))*10)
    camera.look_at(PyGame3d.Vector3(0,-4,0))
# tickerに追加
func_id = game.stage.ticker_add(update)
# おまじない（while文スタート ）
game.start_rendering()