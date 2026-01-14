# 環境構築
```sh
python3.14 -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
python3.14 main.py
```   
# 起動
python3.14を指定していますが、python3コマンドでもversionが最新であれば動きます（多分）
```sh
source ./.venv/bin/activate
python3.14 main.py
```
# 使い方
main.py
```py
# include<>
import PyGame3d
import math
from PyGame3d.GameObject.Cube import Cube,Floor,CuttingBoad
from PyGame3d.GameObject.obj import UVColorMesh_Sprite3D
from PyGame3d.GameObject import GameContainer
from PyGame3d.vector import Vector3

# おまじない
game = PyGame3d.Application()
game.init() 

# 変数定義
angle = 0.0
# ゲーム内オブジェクトを定義
cube = Cube()
floor = Floor()
floor.set_position(Vector3(0,-5,0))
useTextureObj = UVColorMesh_Sprite3D("./Assets/tex.png","./Assets/u.obj")
game.stage.camera.position = Vector3(0,0,10)
cutting = CuttingBoad("./Assets/tex.png")
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
```

なお`GameScript`を継承した関数をstageに追加することでもupdateとstart関数を使うことができます。
# 実装したいことlist
- [x] Mesh型作成
- [ ] シングルトン
- [x] Cube型作成
- [ ] GUI操作実装
- [ ] カスタムシェーダー実装
- [ ] 衝突判定実装
- [ ] 物理演算実装
- [ ] 2d ui を使えるGameContainer型の実装

## よく使うclass一覧

### class Application 
  - scene
  - shader_program
  - context (ctx)

pygameのセットアップとツリー構造の大元の生成を担うクラスです。

最も最初に呼び出して下さい。

- def init 
 
最後にメインループを開始するときに呼び出して下さい。

この関数の実行後は以降の処理が読み込まれないことに注意して下さい。

- def start_rendering

### class Scene

  - execute_objects (exe)
  - container 
  - event
  - camera

containerの大元となるオブジェクトです。

このオブジェクトをインスタンス化することで、全く別のゲーム画面を実装可能です。

### class GameContainer 
  - position
  - rotation
  - scale
  
子要素の追加・削除

  - def remove_child (ContainerComponent)
    - 計算量O(n)で実装されているので覚悟して下さい。
  - def add_child (Game)

localな値を使用する場合に対応するため、全てのTransform系のComponentはGameContainerで実装されています。

### class Sprite3D extends GameContainer
  - mesh
 
描画するためのポリゴンデータを持っています。

### class Cube extends Sprite3D

コンストラクタにてmeshに立方体のポリゴンを渡しています。

### class Sprite3D_obj_format extends Sprite3D

コンストラクタにて.obj形式で渡した値を読み込んで描画できるように実装されています。

## 内部的な処理として使いたい Class

- class VertColorMesh
  - 保持する行列が [x,y,z,r,g,b] の行列
  - .objファイルの形のデータにだけ対応
- class ShaderContainer 
  - moderngl の Context と Program を保持
  - 使用するメッシュによって使い分けるための class

## 開発中

class UVMesh
  - 保持する行列が [x,y,z,u,v] の行列
  - .objのTextureに対応

## 未開発