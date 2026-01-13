import moderngl
from PyGame3d.Draw.shader_container import ShaderContainerComponent
from PyGame3d.Draw.vcolormesh import MeshLike , MeshRender
from PyGame3d.Draw import MeshLike,MeshRender
import numpy as np
import PyGame3d.static as static
class UVMesh (MeshRender,MeshLike):
    ctx : moderngl.Context
    shader : ShaderContainerComponent
    vbo : moderngl.Buffer
    vao : moderngl.VertexArray
    def __init__(self ,vertices:np.ndarray) -> None:
        if static.context is None or static.uv_mesh is None :
            raise
        self.ctx = static.context
        self.shader = static.uv_mesh
        self.vbo = self.ctx.buffer(vertices.astype('f4').tobytes())
        content = [(self.vbo, '3f 2f', 'in_vert', 'in_uv')]
        self.vao = self.ctx.vertex_array(self.shader, content)