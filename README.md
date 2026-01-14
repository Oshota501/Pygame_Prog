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

```
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