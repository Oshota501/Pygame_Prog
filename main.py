# include<>
import PyGame3d
import math
from PyGame3d.Draw.meshmaker import CreativeUVMesh
from PyGame3d.Draw.uvmesh import UVMaterial, UVTexture, UVTextureImage
from PyGame3d.GameObject.Cube import Cube,Floor,CuttingBoad
from PyGame3d.GameObject.obj import UVColorMesh_Sprite3D
from PyGame3d.GameObject import GameContainer, Sprite3D
from PyGame3d.vector import Vector3

# おまじない
game = PyGame3d.Application()
game.init() 

# 変数定義
angle = 0.0
# ゲーム内オブジェクトを定義
cube = Cube()
floor = Floor.include_transform(position=Vector3(0,-5,0))
useTextureObj = UVColorMesh_Sprite3D("./Assets/tex.png","./Assets/u.obj")
game.stage.camera.position = Vector3(0,0,10)
cutting = CuttingBoad("./Assets/tex.png")

mat_wall = UVMaterial.include_texture([
    UVTextureImage(filepath="./Assets/py.png")
])
creative = CreativeUVMesh (mat_wall)
creative.set_squarea()
creative.create()
c_obj = [
    Sprite3D.include_transform(position=Vector3(0,0,14)),
    Sprite3D.include_transform(position=Vector3(0,0,-14)),
    Sprite3D.include_transform(position=Vector3(14,0,0)),
    Sprite3D.include_transform(position=Vector3(-14,0,0))
]
for c in c_obj :
    c.mesh = creative
# コンテナ定義
container = GameContainer()
# コンテナに追加
container.add_children([useTextureObj,cube,floor,cutting,*c_obj])
# stageに追加
game.stage.add_child(container)
# update関数定義
def update (delta_MS:float) -> None :
    global angle
    angle += delta_MS * 0.001
    game.stage.camera.position = Vector3(math.sin(angle),0,math.cos(angle))*10
    for c in c_obj :
        c.scale = Vector3(4,2,4)*(math.cos(angle*15)+1) + Vector3(4,2,4)
        c.look_at(game.stage.camera.position)
    game.stage.camera.look_at(Vector3(0,0,0))
# tickerに追加
func_id = game.stage.ticker_add(update)
# おまじない（while文スタート ）
game.start_rendering()
