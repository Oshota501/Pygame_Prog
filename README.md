# 環境構築

```sh
python3.14 -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
python3.14 main.py
```

## 起動

python3.14を指定していますが、python3コマンドでもversionが最新であれば動きます（多分）

```sh
source ./.venv/bin/activate
python3.14 main.py
```

## 使い方

### パフォーマンスについて

numpyのndarrayを使用したMatrix4とcppで自作したMatrix4が存在しています。（どちらも全く同じ実装です。）

デフォルトで前者を使用するようにしていますが、後者の方が若干パフォーマンス的に速度が出るかもしれません。

- コンパイル
```sh
sh setup.sh
```
- 変更
`/PyGame3d/__init__.py`
```py
from .matrix.mat4 import Matrix4
```
を
```py
from .pg3_math.matrix import Matrix4
```
に変更

### 簡単な使い方

main.py

```py
# include<>
import PyGame3d
import math
# おまじない
game = PyGame3d.Application(check_performance=True)
game.init() 
camera = game.stage.get_camera()
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
useTextureObj = PyGame3d.Sprite3D.obj("./Assets/a.obj","./Assets/tex.png")
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
    
    angle += delta_time
    camera.position = PyGame3d.Vector3(math.sin(angle),0,math.cos(angle))*10
    camera.look_at(PyGame3d.Vector3(0,0,0))
# tickerに追加
func_id = game.stage.ticker_add(update)
# おまじない（while文スタート ）
game.start_rendering()

```

なお`GameScript`を継承した関数をstageに追加することでもupdateとstart関数を使うことができます。

### ゲームの画面を使い分けたい場合

**注意：仕様を変更したため、サポートされていません**

```py
# import
import PyGame3d
import math
from PyGame3d import Scene
from PyGame3d.GameObject.Cube import Cube, Floor,CuttingBoad
from PyGame3d.GameObject import GameContainer
from PyGame3d.GameObject.sprite import Sprite3D
from PyGame3d.vector import Vector3

# おまじない
game = PyGame3d.Application()
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
        self.sprite = Sprite3D.obj("./Assets/u.obj","./Assets/tex.png")
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
```

## 実装したいことlist

- [x] Mesh型作成
- [x] シングルトン
- [x] Cube型作成
- [ ] GUI操作実装
- [ ] カスタムシェーダー実装
- [x] 衝突判定実装
- [ ] 物理演算実装 (NEXT)
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
