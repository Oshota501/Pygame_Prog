import os
import moderngl
import pygame
from PyGame3d.Draw import MaterialLike, TextureLike
from PyGame3d.Draw.uvmesh import UV3dShaderContainer


class UVTexture (TextureLike):
    ctx : moderngl.Context
    texture : moderngl.Texture
    def __init__(self, context:moderngl.Context,texture:moderngl.Texture) -> None:
        self.ctx = context  
        self.texture = texture
    @staticmethod
    def get_context () -> moderngl.Context :
        from PyGame3d import static
        if static.context is None :
            raise ValueError("please execute Application.init()")
        return static.context
    def use(self, location):
        self.texture.use(location=location)
    def get(self) -> moderngl.Texture:
        return self.texture

    @classmethod
    def color(cls, color: tuple[float, float, float] | tuple[float, float, float, float], size: tuple[int, int] = (1, 1)) -> "UVTexture":
        """指定色から単色テクスチャを生成する。colorは0.0～1.0のRGBA/ RGBタプル。"""
        from PyGame3d import static
        if static.context is None:
            raise ValueError("please execute Application.init()")
        ctx = static.context
        a = color[3] if len(color) == 4 else 1.0
        rgba8 = (
            int(max(0.0, min(1.0, color[0])) * 255),
            int(max(0.0, min(1.0, color[1])) * 255),
            int(max(0.0, min(1.0, color[2])) * 255),
            int(max(0.0, min(1.0, a)) * 255),
        )
        surface = pygame.Surface(size, flags=pygame.SRCALPHA)
        surface.fill(rgba8)
        surface = pygame.transform.flip(surface, False, True)
        tex = ctx.texture(
            size=size,
            components=4,
            data=pygame.image.tobytes(surface, "RGBA"),
        )
        tex.filter = (moderngl.LINEAR, moderngl.LINEAR)
        tex.build_mipmaps()
        inst = cls.__new__(cls)
        inst.ctx = ctx
        inst.texture = tex
        return inst
    
    @staticmethod
    def empty () -> UVTexture:
        ctx = UVTexture.get_context()
        return UVTexture(
            ctx ,
            ctx.texture(
                size=(0,0),
                components=4
            )
        )
class UVTextureImage (UVTexture,TextureLike) :
    # override
    def __init__(self, filepath: str) -> None:   
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Texture file not found: {filepath}")
        self.ctx = UVTexture.get_context()
        surface = pygame.image.load(filepath).convert_alpha()
        surface = pygame.transform.flip(surface, False, True)
        self.texture = self.ctx.texture(
            size=surface.get_size(),
            components=4, # RGBなら3, RGBAなら4
            data=pygame.image.tobytes(surface, 'RGBA')
        )
        self.texture.filter = (moderngl.LINEAR, moderngl.LINEAR)
        self.texture.build_mipmaps()

class UVMaterial (MaterialLike):
    program : moderngl.Program
    textures : dict[int,TextureLike]
    uniform_name : str
    def __init__(self):
        uv_mesh = UV3dShaderContainer()
        program = uv_mesh.get_program()
        if program is None :
            raise ValueError("Please execute Application.init ()")
        self.program = program
        self.textures = {} # { location_index: TextureObject } の辞書
        self.uniform_name = "u_texture"  # デフォルト値

    def add_texture(self, texture:UVTexture, location:int, uniform_name:str="u_texture"):
        """
        テクスチャを登録する
        texture: Textureインスタンス
        location: 0, 1, 2...
        uniform_name: シェーダー内の変数名 ("u_texture" など)
        """
        self.textures[location] = texture
        self.uniform_name = uniform_name
    def add_color_texture(self, color: tuple[float, float, float] | tuple[float, float, float, float], location:int=0, uniform_name:str="u_texture"):
        """単色テクスチャを登録するヘルパー。"""
        tex = UVTexture.color(color)
        self.add_texture(tex, location, uniform_name)

    def use(self):
        """描画直前に呼ぶ：登録された全テクスチャをバインドする"""
        # テクスチャをバインド
        for loc, tex in self.textures.items():
            tex.use(location=loc)
        # uniformにテクスチャユニットのインデックスを設定（最初のテクスチャを使用）
        if self.textures and self.uniform_name in self.program:
            first_location = min(self.textures.keys())
            self.program[self.uniform_name].value = first_location # type:ignore
    def get_textures(self) -> dict[int, TextureLike]:
        return self.textures
    @staticmethod
    def include_texture(texs:list[UVTexture]) -> UVMaterial:
        m = UVMaterial()
        for i,t in enumerate(texs) :
            m.add_texture(t,i)
        return m
    @staticmethod
    def img_mono_texture (filename:str) -> UVMaterial :
        tex = UVTextureImage(filepath=filename)
        return UVMaterial.include_texture([tex])
