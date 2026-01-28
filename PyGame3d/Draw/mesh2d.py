import moderngl
import numpy as np
from PyGame3d import matrix
from PyGame3d.Draw import MaterialLike, MeshLike, MeshRender, TextureLike, Transform
from PyGame3d.Draw.shader_container import ShaderContainer
from PyGame3d.Scene.component import SceneComponent
from PyGame3d.Singleton import SingletonABCMeta
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from PyGame3d.game import Application

# signature : oshota
from PyGame3d.matrix.mat4 import Matrix4
from PyGame3d.vector import Vector2
from PyGame3d.Draw.texture import UVTexture 
# coded by oshota
class Mesh2dShaderContainer(ShaderContainer, metaclass=SingletonABCMeta):
    def __init__(self,
            vertpath: str="./PyGame3d/shaderprogram/2d.vert",
            fragpath: str="./PyGame3d/shaderprogram/2d.frag"
    ) -> None:
        try :
            frag : str
            vert : str
            with open(vertpath,"r") as vertshader :
                with open(fragpath,"r") as fragmentshader :
                    vert = vertshader.read()
                    frag = fragmentshader.read()
            super().__init__(vert, frag)
        except :
            raise FileExistsError(f"ShaderProgram is not found.\n{fragpath}\n{vertpath}")

    def start(self, game: Application) -> None:
        # 1. 画面サイズを取得
        width, height = game.screen_size
        
        # 2. 2D用の正射影行列を作成
        ortho_mat = matrix.create_ortho(0, width, height, 0, -1.0, 1.0)
        
        # 3. シングルトンのMesh2dShaderContainerに送信
        from PyGame3d.Draw.mesh2d import Mesh2dShaderContainer
        Mesh2dShaderContainer().send_ortho(ortho_mat)

    def update(self, scene:SceneComponent) -> None:
        # デフォルト値
        if 'color_tint' in self.program:# type: ignore
            self.program['color_tint'].value = (1.0, 1.0, 1.0, 1.0) # type: ignore
        else :
            raise ValueError("Shader does not have 'color_tint' uniform .")
        if 'texture0' in self.program:# type: ignore
            self.program['texture0'].value = 0 # type: ignore
        else :
            raise ValueError("Shader does not have 'texture0' uniform .")

    def send_ortho(self, ortho_matrix: Matrix4) -> None:
        self.send_uniform("proj", ortho_matrix)
# Coded By Gemini
class Mesh2dMaterial(MaterialLike):
    program: moderngl.Program
    textures: dict[int, TextureLike]
    uniform_name: str

    def __init__(self):
        # 2D用のシェーダーコンテナからプログラムを取得
        shader = Mesh2dShaderContainer()
        program = shader.get_program()
        if program is None:
            raise ValueError("Shader Program not found. Ensure Mesh2dShaderContainer is initialized.")
        
        self.program = program
        self.textures = {}
        # 2Dシェーダーで使われているsampler2Dの名前 (通常は texture0)
        self.uniform_name = "texture0" 

    def add_texture(self, texture: TextureLike, location: int, uniform_name: str = "texture0"):
        self.textures[location] = texture
        self.uniform_name = uniform_name

    def use(self):
        """描画直前に呼ぶ：登録された全テクスチャをバインドする"""
        for loc, tex in self.textures.items():
            tex.use(location=loc)
        
        # シェーダーにlocationを通知
        if self.textures and self.uniform_name in self.program:
            first_location = min(self.textures.keys())
            self.program[self.uniform_name].value = first_location # type: ignore

    def get_textures(self) -> dict[int, TextureLike]:
        return self.textures

    @staticmethod
    def from_texture(texture: TextureLike) -> "Mesh2dMaterial":
        """テクスチャ1枚からマテリアルを簡易作成するヘルパー"""
        mat = Mesh2dMaterial()
        mat.add_texture(texture, 0)
        return mat

# Coded By Gemini
class Mesh2d(MeshRender, MeshLike):
    ctx: moderngl.Context
    shader: Mesh2dShaderContainer
    material: Mesh2dMaterial 
    vbo: moderngl.Buffer
    vao: moderngl.VertexArray

    def __init__(self, material: Mesh2dMaterial, width: float, height: float, pivot_center: bool = True) -> None:
        from PyGame3d import static
        if static.context is None:
            raise ValueError("Please execute Application.init()")
        
        self.ctx = static.context
        
        # シングルトンシェーダーを取得
        self.shader = Mesh2dShaderContainer()
        self.material = material

        w, h = width, height
        if pivot_center:
            # 中心基準の場合も、Y軸の向きに注意
            l, r, t, b = -w/2, w/2, -h/2, h/2 # 上がマイナス、下がプラス
        else:
            # 左上基準の場合
            l, r, t, b = 0, w, 0, h

        # 頂点データ (x, y, u, v)
        vertices = np.array([
            l, t, 0.0, 1.0,
            l, b, 0.0, 0.0,
            r, t, 1.0, 1.0,
            
            l, b, 0.0, 0.0,
            r, b, 1.0, 0.0,
            r, t, 1.0, 1.0,
        ], dtype='f4')

        self.vbo = self.ctx.buffer(vertices.tobytes())
        content = [(self.vbo, '2f 2f', 'in_vert', 'in_uv')]
        self.vao = self.ctx.vertex_array(self.shader.program, content)

    def render(self, transform: Transform) -> None:
        # マテリアルを適用 (テクスチャバインド等)
        # しんどテスト無効
        self.ctx.disable(moderngl.DEPTH_TEST)
        self.ctx.disable(moderngl.CULL_FACE)
        self.material.use()
        
        model_mat = (
            matrix.create_translation(transform.position.x, transform.position.y, 0) *
            matrix.create_scale(transform.scale.x, transform.scale.y, 1)
        )

        # シェーダーへの送信
        if 'model' in self.shader.program: # type: ignore
            self.shader.program['model'].write(model_mat.tobytes()) # type: ignore
        else :
            raise ValueError("Shader does not have uniform 'model'")
        self.vao.render()
        self.ctx.enable(moderngl.DEPTH_TEST)
        self.ctx.enable(moderngl.CULL_FACE)
        
    def set_color_tint(self, r, g, b, a):
        # tintはUniformなのでシェーダーに対して直接送るか、マテリアルに機能を持たせる
        # 現状はシェーダーコンテナ経由で送信
        if 'color_tint' in self.shader.program: #type:ignore
            self.shader.program['color_tint'].value = (r, g, b, a) # type: ignore
        else :
            raise ValueError("Shader does not have uniform 'color_tint'")

    def destroy(self):
        self.vbo.release()
        self.vao.release()

    def get_material(self) -> MaterialLike | None:
        return self.material

    def get_render_obj(self) -> tuple[moderngl.Context, moderngl.Program] | None:
        if self.shader.context is None or self.shader.program is None :
            return None
        return (
            self.shader.context ,
            self.shader.program
        )
    # coded by oshota
    @staticmethod
    def color_rect(color: tuple[float, float, float, float], size: Vector2) -> "Mesh2d":
        # Texture作成 -> Material作成 -> Mesh作成 の順序
        texture = UVTexture.color(color)
        material = Mesh2dMaterial.from_texture(texture)
        return Mesh2d(material, size.x, size.y, pivot_center=False) 

    @staticmethod
    def color_rectangle(color: tuple[float, float, float, float], size: Vector2) -> "Mesh2d":
        return Mesh2d.color_rect(color, size)
    
    @staticmethod
    def image_rect(filepath: str, size: Vector2) -> "Mesh2d":
        from PyGame3d.Draw.texture import UVTextureImage
        texture = UVTextureImage(filepath)
        material = Mesh2dMaterial.from_texture(texture)
        return Mesh2d(material, size.x, size.y, pivot_center=True)

    # Coding By Gemini
    @staticmethod
    def text(
        text: str, 
        font_size: int = 24, 
        color: tuple[int, int, int] = (255, 255, 255), 
        font_path: str | None = None
    ) -> "Mesh2d":
        """
        文字列からMesh2dを生成する (Pillow使用)
        """
        from PyGame3d import static
        from PyGame3d.Draw.texture import UVTexture # 必要に応じてimportパス調整
        from PIL import ImageFont,Image,ImageDraw
        
        if static.context is None:
            raise ValueError("Please execute Application.init()")
        ctx = static.context

        # 1. フォントのロード (Pillow)
        try:
            if font_path:
                font = ImageFont.truetype(font_path, font_size)
            else:
                print("\033[33mWarning : Font path does not set right.")
                # デフォルトフォントの読み込み試行
                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                except:
                    font = ImageFont.load_default()
        except OSError:
            font = ImageFont.load_default()
            print("\033[33mWarning : Font path does not set right.")

        # 2. テキストサイズの計算
        bbox = font.getbbox(text)
        text_width = int(bbox[2])
        # bbox[3]はベースラインより下の高さなので、bbox[1](上の余白)も考慮する場合があるが
        # getbboxの仕様に合わせて高さを確保
        text_height = int(bbox[3] - bbox[1] + 5) # 少し余裕を持たせる

        # 画像サイズ (余白を持たせる)
        w, h = text_width + 4, text_height + 10

        # 3. Pillowで画像生成 (RGBA, 背景透明)
        image = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # 文字描画 (位置調整)
        draw.text((2, 0), text, font=font, fill=color + (255,))

        # 4. 上下反転 (OpenGLのUV座標系 V=0が下 に合わせる)
        # ※Mesh2dのUV設定(左上がV=1.0)なら、画像は「正位置」でOKな場合もありますが、
        #  OpenGLのテクスチャデータ転送は通常「左下原点」で行われるため、反転が必要なケースが多いです。
        #  もし文字が上下逆さまに出たら、この行をコメントアウトしてください。
        image = image.transpose(Image.FLIP_TOP_BOTTOM) # type:ignore

        # 5. ModernGLテクスチャの生成
        texture_data = image.tobytes("raw", "RGBA")
        tex = ctx.texture((w, h), 4, texture_data)
        tex.filter = (moderngl.LINEAR, moderngl.LINEAR)
        
        # 6. UVTextureラッパーの生成 (__new__ハックで無理やり生成)
        uv_tex = UVTexture.__new__(UVTexture)
        uv_tex.ctx = ctx
        uv_tex.texture = tex
        
        # 7. Materialの生成
        material = Mesh2dMaterial.from_texture(uv_tex)
        
        # 8. Mesh2dを返す (pivot_center=Trueなら中心基準、Falseなら左上基準)
        # 文字列はUIとして左上基準で配置したいことが多いので False にしています
        return Mesh2d(material, w, h, pivot_center=True)
