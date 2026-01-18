from abc import abstractmethod
from PyGame3d.Draw import MeshLike, TextureLike, Transform
from PyGame3d.GameObject import (
    CollisionDetectionContainer, 
    GameContainer, 
    Sprite3DComponent,
    BoundingObject,
    BoundingShape,
    AxisAlignedBoundingBox,
    BoundingSphere,
    SimpleBoundingObject
)
from PyGame3d.vector import Vector3
import math

# signature : oshota
class Sprite3DBoundingObject(BoundingObject):
    sprite: "Sprite3D"
    
    def __init__(self, sprite: "Sprite3D") -> None:
        self.sprite = sprite
    
    def bounding(self) -> BoundingShape:
        """Sprite3Dの位置とスケールからAABBを計算する。"""
        position = self.sprite.get_position()
        scale = self.sprite.get_scale()
        
        # スケールを考慮した最小点と最大点を計算
        # 簡易実装: スケールの半分を半径として使用
        half_size = Vector3(abs(scale.x) / 2.0, abs(scale.y) / 2.0, abs(scale.z) / 2.0)
        min_point = position - half_size
        max_point = position + half_size
        
        return AxisAlignedBoundingBox(min_point, max_point)

class Sprite3D (
    GameContainer,
    Sprite3DComponent,
    CollisionDetectionContainer
) :
    mesh : MeshLike | None
    _collide_enabled : bool
    _bounding_obj : list[Sprite3DBoundingObject]
    
    def __init__(self,name="Sprite") -> None:
        # GameContainerの__init__を呼ぶ（位置やスケールの初期化）
        GameContainer.__init__(self, name)
        # CollisionDetectionContainerの__init__を明示的に呼ぶ（CollisionManagerへの登録）
        CollisionDetectionContainer.__init__(self)
        self.mesh = None
        self._collide_enabled = False  # デフォルトで衝突判定を無効にする
        self._bounding_obj = []
    # @override
    def update(self,delta_MS:float):
        super().update(delta_MS)
        if self.mesh is not None :
            self.mesh.render(Transform(
                self.get_position(),
                self.get_rotation(),
                self.get_scale()
            ))
        # else :
        #     print("not set mesh")
    def get_mesh(self) -> MeshLike|None:
        return self.mesh 
    # CollisionDetectionContainer の実装
    def is_collide_valid(self) -> bool:
        return self._collide_enabled
    
    def set_collide_enabled(self, enabled: bool) -> None:
        self._collide_enabled = enabled
    def set_bounding_obj(self, obj: BoundingObject) -> None:
        self._bounding_obj = [obj]
        
    def get_bounding_obj(self) -> list[BoundingObject]:
        # # _bounding_objが空の場合は、Sprite3DBoundingObjectを自動追加
        # if len(self._bounding_obj) == 0 and self._collide_enabled:
        #     self._bounding_obj.append(Sprite3DBoundingObject(self))
        
        # SimpleBoundingObjectの位置とスケールを更新
        position = self.get_position()
        scale = self.get_scale()
        for bound_obj in self._bounding_obj:
            if isinstance(bound_obj, SimpleBoundingObject):
                bound_obj.set_position(position)
                bound_obj.set_scale(scale)
        
        return self._bounding_obj

    def collide(self,other:CollisionDetectionContainer) -> None:
        """you can use function when collided .please over ride."""
        return

    # static method
    @staticmethod
    def transform (
            position=Vector3(0,0,0),
            rotation=Vector3(0,0,1),
            scale=Vector3(1,1,1)
    ) -> Sprite3D :
        g = Sprite3D()
        g.set_position(position)
        g.set_rotation(rotation)
        g.set_scale(scale)
        return g
    @staticmethod
    def obj(obj_filename:str,texture_filename:str|None=None) -> Sprite3D :
        from PyGame3d.Draw.uvmesh import UVTextureImage,UVMaterial,UVMesh,UVTexture
        import os
        result = Sprite3D()
        tex_wall : TextureLike
        if texture_filename is None :
            tex_wall = UVTexture.color((0,1,0))
        else :
            if not os.path.exists(texture_filename):
                raise FileNotFoundError(f"Texture file not found: {texture_filename}")
            tex_wall = UVTextureImage(filepath=texture_filename)
        mat_wall = UVMaterial()
        mat_wall.add_texture(tex_wall,0)
        if not os.path.exists(obj_filename):
            raise FileNotFoundError(f"Object file not found: {obj_filename}")
        result.mesh = UVMesh.load_obj(mat_wall,obj_filename=obj_filename)
        return result