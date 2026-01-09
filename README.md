# 環境構築
```sh
python3.14 -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
python3.14 main.py
```   
# 起動
```sh
source ./.venv/bin/activate
python3.14 main.py
```

# 実装したいことlist
- [x] Mesh型作成
- [ ] シングルトン
- [ ] Cube型作成
- [ ] GUI操作実装
- [ ] カスタムシェーダー実装
- [ ] 衝突判定実装
- [ ] 物理演算実装
  
## 実装したい


抽象class GameObjectRender

- render()->None

抽象class HierarchicalGameObject

- get_position() -> vec3

class GameManager 

- update

- start

- これを継承しているclassは自動でupdateやstartが描画処理のwhile文の中で実行されるようにしたい。

class GameObject implements GameObjectRender,HierarchicalGameObject

- position (vec3)

- scale (vec3)

- translate (vec3)

- Mesh

- destroy

- Meshを持っている。小要素を持てない。

class GameObjectFolder implements GameObjectRender

- list[GameObjectRender]

- addChild

- removeChild

- clear

- GameObjectの配列を持っている。

class GameObjectContainer implements GameObjectRender,HierarchicalGameObject

- position 

- list[HierarchicalGameObject]

- addChild

- removeChild

- 複数のゲームオブジェクトをまとめて動かしたいときにコンテナに梱包することで小要素のpositionを自動的にlocalpositionとする