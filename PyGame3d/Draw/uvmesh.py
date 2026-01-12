import moderngl
from PyGame3d.Draw.vcolormesh import MeshLike , MeshRender
from PyGame3d.Draw import MeshLike,MeshRender,Transform
import numpy as np

class UVMesh (MeshRender,MeshLike):
    ctx : moderngl.Context
    program : moderngl.Program
    vbo : moderngl.Buffer
    vao : moderngl.VertexArray
    def __init__(self, ctx:moderngl.Context, program:moderngl.Program, vertices:np.ndarray) -> None:
        self.ctx = ctx
        self.program = program
        self.vbo = self.ctx.buffer(vertices.astype('f4').tobytes())
        content = [(self.vbo, '3f 2f', 'in_vert', 'in_uv')]
        self.vao = self.ctx.vertex_array(self.program, content)