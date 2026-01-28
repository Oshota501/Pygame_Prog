import moderngl
from PyGame3d import matrix
from PyGame3d import static
from PyGame3d.Draw import MeshLike, TextureLike, Transform
from PyGame3d.Draw.shader_container import ShaderContainer
from PyGame3d.Singleton import SingletonABCMeta
from PyGame3d.matrix.mat4 import Matrix4
import numpy as np

class Mesh2dShaderContainer (
    ShaderContainer,
    metaclass=SingletonABCMeta
) :
    def __init__(self,
            vertpath: str="./PyGame3d/shaderprogram/mesh2d.vert",
            fragpath: str="./PyGame3d/shaderprogram/mesh2d.frag"
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
            print("Not found shader program text file.")
    
    def update(self, scene) -> None:
        # 2D描画ではカメラ(View)の影響を受けない（あるいはスクロール用のみ）
        # ここではデフォルト値をセット
        self.program['color_tint'].value = (1.0, 1.0, 1.0, 1.0) # type: ignore
        self.program['texture0'].value = 0 # type: ignore

    # 2D用の正射影行列を送るメソッド（既存のsend_perspectiveを流用しても良いが区別するため）
    def send_ortho(self, ortho_matrix: Matrix4) -> None:
        self.send_uniform("proj",ortho_matrix)

# --- 2Dメッシュクラス ---
class Mesh2d(MeshLike):
    ctx: moderngl.Context
    shader: Mesh2dShaderContainer
    material_tex: TextureLike
    vbo: moderngl.Buffer
    vao: moderngl.VertexArray

    # 幅と高さを持つ矩形を作成
    def __init__(self, texture: TextureLike, width: float, height: float, pivot_center: bool = True) -> None:
        if static.context is None:
            raise ValueError("Please execute Application.init()")
        
        self.ctx = static.context
        
        # もし未ロードならシェーダーを読み込む（シングルトン的な管理推奨）
        # ここでは簡易的に都度確認

        self.shader = static.mesh_2d # type:ignore
        self.material_tex = texture

        # 頂点データ生成 (x, y, u, v)
        # pivot_center: Trueなら中心が(0,0)、Falseなら左上が(0,0)
        w, h = width, height
        if pivot_center:
            l, r, t, b = -w/2, w/2, h/2, -h/2
        else:
            l, r, t, b = 0, w, 0, -h # Y軸は上がプラスか下がプラスか、投影行列次第

        # GLの標準的なUV座標 (左下原点想定ならVを反転など調整)
        vertices = np.array([
            # x, y, u, v
            l, t, 0.0, 1.0,  # 左上 (OpenGLのテクスチャ座標系に合わせて調整してください)
            l, b, 0.0, 0.0,  # 左下
            r, t, 1.0, 1.0,  # 右上
            
            l, b, 0.0, 0.0,  # 左下
            r, b, 1.0, 0.0,  # 右下
            r, t, 1.0, 1.0,  # 右上
        ], dtype='f4')

        self.vbo = self.ctx.buffer(vertices.tobytes())
        
        # 2D用は '2f 2f' (pos2, uv2)
        content = [(self.vbo, '2f 2f', 'in_vert', 'in_uv')]
        self.vao = self.ctx.vertex_array(self.shader.program, content)

    def render(self, transform: Transform) -> None:
        self.material_tex.use(location=0)
        
        # モデル行列（2D位置）の計算
        # 2DなのでZ回転だけを使うことが多いが、汎用的に回転行列を使う
        model_mat = (
            matrix.create_translation(transform.position.x, transform.position.y, 0) *
            # ここに必要な回転行列 *
            matrix.create_scale(transform.scale.x, transform.scale.y, 1)
        )

        self.shader.program['model'].write(model_mat.tobytes()) # type: ignore
        self.vao.render()
        
    def set_color_tint(self, r, g, b, a):
        self.shader.program['color_tint'].value = (r, g, b, a) # type: ignore

    def destroy(self):
        self.vbo.release()
        self.vao.release()