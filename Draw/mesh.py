import numpy as np
import moderngl
from typing import cast
class Mesh :
    ctx : moderngl.Context
    program : moderngl.Program
    vbo : moderngl.Buffer
    vao : moderngl.VertexArray
    def __init__(self, ctx:moderngl.Context, program:moderngl.Program, vertices:np.ndarray) -> None:
        self.ctx = ctx
        self.program = program
        self.vbo = self.ctx.buffer(vertices.astype('f4').tobytes())
        content = [(self.vbo, '3f 3f', 'in_vert', 'in_color')]
        self.vao = self.ctx.vertex_array(self.program, content)
    def render (self, model_matrix=None) -> None:
        # もし位置や回転の行列が渡されたら、シェーダーに送る
        if model_matrix is not None and 'model' in self.program:
            # 以下のignoreが気になるようでしたら、コメントアウトしているコードを使って下さい。
            self.program["model"].write(model_matrix) # type: ignore 
            # write_prog = cast(moderngl.Uniform,self.program["model"])
            # write_prog.write(model_matrix)
        else :
            print ("Shader error .\n Default vertex shader do not exist \"uniform model\" ")
            print ("Could not Registration Model from vert shader.")
            return
        # 描画実行
        self.vao.render()
    def destroy (self) -> None:
        self.vao.release()
        self.vbo.release()
    @staticmethod
    def get_cube_data() -> np.ndarray:
        vertices = [
            # 前面 (z = 0.5) - 赤
            -0.5, -0.5,  0.5, 1.0, 0.0, 0.0,
             0.5, -0.5,  0.5, 1.0, 0.0, 0.0,
             0.5,  0.5,  0.5, 1.0, 0.0, 0.0,
            -0.5, -0.5,  0.5, 1.0, 0.0, 0.0,
             0.5,  0.5,  0.5, 1.0, 0.0, 0.0,
            -0.5,  0.5,  0.5, 1.0, 0.0, 0.0,
            
            # 背面 (z = -0.5) - 緑
             0.5, -0.5, -0.5, 0.0, 1.0, 0.0,
            -0.5, -0.5, -0.5, 0.0, 1.0, 0.0,
            -0.5,  0.5, -0.5, 0.0, 1.0, 0.0,
             0.5, -0.5, -0.5, 0.0, 1.0, 0.0,
            -0.5,  0.5, -0.5, 0.0, 1.0, 0.0,
             0.5,  0.5, -0.5, 0.0, 1.0, 0.0,
            
            # 右面 (x = 0.5) - 青
             0.5, -0.5,  0.5, 0.0, 0.0, 1.0,
             0.5, -0.5, -0.5, 0.0, 0.0, 1.0,
             0.5,  0.5, -0.5, 0.0, 0.0, 1.0,
             0.5, -0.5,  0.5, 0.0, 0.0, 1.0,
             0.5,  0.5, -0.5, 0.0, 0.0, 1.0,
             0.5,  0.5,  0.5, 0.0, 0.0, 1.0,
            
            # 左面 (x = -0.5) - 黄
            -0.5, -0.5, -0.5, 1.0, 1.0, 0.0,
            -0.5, -0.5,  0.5, 1.0, 1.0, 0.0,
            -0.5,  0.5,  0.5, 1.0, 1.0, 0.0,
            -0.5, -0.5, -0.5, 1.0, 1.0, 0.0,
            -0.5,  0.5,  0.5, 1.0, 1.0, 0.0,
            -0.5,  0.5, -0.5, 1.0, 1.0, 0.0,
            
            # 上面 (y = 0.5) - マゼンタ
            -0.5,  0.5,  0.5, 1.0, 0.0, 1.0,
             0.5,  0.5,  0.5, 1.0, 0.0, 1.0,
             0.5,  0.5, -0.5, 1.0, 0.0, 1.0,
            -0.5,  0.5,  0.5, 1.0, 0.0, 1.0,
             0.5,  0.5, -0.5, 1.0, 0.0, 1.0,
            -0.5,  0.5, -0.5, 1.0, 0.0, 1.0,
            
            # 下面 (y = -0.5) - シアン
            -0.5, -0.5, -0.5, 0.0, 1.0, 1.0,
             0.5, -0.5, -0.5, 0.0, 1.0, 1.0,
             0.5, -0.5,  0.5, 0.0, 1.0, 1.0,
            -0.5, -0.5, -0.5, 0.0, 1.0, 1.0,
             0.5, -0.5,  0.5, 0.0, 1.0, 1.0,
            -0.5, -0.5,  0.5, 0.0, 1.0, 1.0,
        ]
        return np.array(vertices, dtype='f4')
