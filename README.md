# 説明

### Pygameの3dライブラリです。

画面とイベント処理は完全にpygameに依存していますが、描画のプロセスにpygameは一切関与しておらず、modernglに依存しています。

# 環境構築

手元にWindowsが都合よくなかったのでMac版のみです。

```sh
python3.14 -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
python3.14 main.py
```

2duiのtextを使う場合は以下のコマンド（MacOS）でフォントのpathを確かめて下さい。

```sh
ls /System/Library/Fonts
```

例えば

```
"/System/Library/Fonts/ヒラギノ角ゴシック W0.ttc"
```

## 起動

python3.14を指定していますが、python3コマンドでもversionが最新であれば動きます（多分）

型定義とかが実装されているpythonを使用して下さい。

```sh
source ./.venv/bin/activate
python3.14 main.py
```

## 使い方

### 概要

1.[class Application](./PyGame3d/game.py) を呼び出してWindowを表示
2.[implements ContainerComponent](./PyGame3d/GameObject/__init__.py)をインスタンス化
- あなたの作る部分
  - [GameContainer](./PyGame3d/GameObject/Container.py)
  - [Sprite3d](./PyGame3d/GameObject/sprite.py)
  - Sample
    - [Cube](./PyGame3d/GameObject/Sample/__init__.py)
    - [Floor](./PyGame3d/GameObject/Sample/__init__.py)
    - [CuttingBoad](./PyGame3d/GameObject/Sample/__init__.py)
    - [FPSPlayer](./PyGame3d/GameObject/Sample/player.py)
- 自動でインスタンスされる
  - [Camera](./PyGame3d/GameObject/Camera.py)
  - [Light](./PyGame3d/GameObject/Light.py)
3.start_rendering()

### 簡単な使い方

main.py

```py
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


```

なお`GameScript`を継承した関数をstageに追加することでもupdateとstart関数を使うことができます。

### ゲームの画面を使い分けたい場合

```py
from PyGame3d import Application, Sprite3D, Floor, Scene, Vector3, CuttingBoad, Cube
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
        self.cube.set_position(Vector3(0, 20, 0))

        self.pygamedenanishitendayo = CuttingBoad("./Assets/py.png")
        self.pygamedenanishitendayo.set_scale(Vector3(20, 4, 1))
        self.pygamedenanishitendayo.set_position(Vector3(0, 0, -10))

        self.gun.look_at(Vector3(0, 0, -1))
        self.gun.set_localposition(Vector3(0.4, -0.3, -0.9))

        self.camera.add_child(self.gun)

        self.add_children(
            Floor.transform(position=Vector3(0, -3, 0)),
            self.cube,
            self.player,
            self.pygamedenanishitendayo,
        )

        print(self.container)
        print(self.cube)

        self.player.set_position(Vector3(0, 10, 3))

    def start(self):
        super().start()

    def update(self, delta_time: float):
        super().update(delta_time)


game.set_scene(StartScene())
PerformanceInspectator(game)
# おまじない（while文スタート ）
game.start_rendering()

```

### ~~パフォーマンスについて~~

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

## 実装したいことlist

- [x] Mesh型作成
- [x] シングルトン
- [x] Cube型作成
- [x] GUI操作実装
- [ ] カスタムシェーダー実装
- [x] 衝突判定実装
- [x] 物理演算実装 (NEXT)
- [x] 2d ui を使えるGameContainer型の実装

## よく使うclass一覧

### [class Vector3](./PyGame3d/vector/Vector3.py)

### [class Quaternion](./PyGame3d/vector/Quaternion.py)

### [class Application](./PyGame3d/game.py)

- __init__ () -> None
  - 変数の初期化

- init () -> None
  - setupをします。

- start_rendering () -> None
  - renderingをstartします。これ以降のコードは読み取られないことに気をつけて下さい。

- def

### [class Scene](./PyGame3d/Scene/__init__.py)

- container
- camera
- get_camera () -> Camera
- light
- get_light () -> list[Light]
- start () -> None
- update () -> None

containerの大元となるオブジェクトです。

このオブジェクトをインスタンス化することで、全く別のゲーム画面を実装可能です。

### [class GameContainer](./PyGame3d/GameObject/Container.py)

- position
- rotation
- scale

- remove_child (ContainerComponent) -> None
  - 計算量O(n)で実装されているので覚悟して下さい。
- def add_child (ContainerComponent)
- update (float delta_time) -> None
- start () -> None
- look_at () -> None

localな値を使用する場合に対応するため、全てのTransform系のComponentはGameContainerで実装されています。

### [class Sprite3D extends GameContainer](./PyGame3d/GameObject/sprite.py)

- mesh


## より低レイヤー Class

### [Mesh](./PyGame3d/Draw/__init__.py)

- [UVMesh](./PyGame3d/Draw/uvmesh.py)
- [VColorMesh](./PyGame3d/Draw/vcolormesh.py)
- [Mesh2d](./PyGame3d/Draw/mesh2d.py)

### [ShaderContainer](./PyGame3d/Draw/shader_container.py)

- Mesh型の上に記載
- [UVMesh](./PyGame3d/Draw/uvmesh.py)
- [VColorMesh](./PyGame3d/Draw/vcolormesh.py)
- [Mesh2d](./PyGame3d/Draw/mesh2d.py)

### [Texture](./PyGame3d/Draw/texture.py)

- UVTexture

### [Material](./PyGame3d/Draw/texture.py)

-UVMaterial

## 開発中

## 未開発
