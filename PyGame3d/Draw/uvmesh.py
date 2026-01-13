import moderngl
import pygame
import numpy as np
import os

from PyGame3d.Draw.shader_container import ShaderContainerComponent
from PyGame3d.Draw import MaterialLike, MeshLike, MeshRender, Transform, TextureLike

import PyGame3d.static as static
import PyGame3d.matrix as matrix
import PyGame3d.matrix.rotation as rmatrix


def load_obj(filename:str) -> np.ndarray:
    vertices:list[list[float]] = [] # v
    tex_coords:list[list[float]] = [] # vt
    
    # 最終的なGPU用の配列 (x, y, z, u, v)
    final_data :list[float]= []

    with open(filename, 'r') as file:
        for line in file:
            parts = line.split()
            if not parts:
                continue

            # 頂点座標 (v x y z)
            if parts[0] == 'v':
                vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
            
            # テクスチャ座標 (vt u v)
            elif parts[0] == 'vt':
                # v (縦方向) はOpenGLでは上下逆になることが多いので、1.0 - v したりします
                # いったんそのまま読みます
                tex_coords.append([float(parts[1]), float(parts[2])])

            # 面情報 (f v1/vt1/vn1 ...)
            elif parts[0] == 'f':
                for i in range(1, 4):
                    vals = parts[i].split('/')
                    v_idx = int(vals[0]) - 1
                    xyz = vertices[v_idx]
                    if len(vals) > 1 and vals[1] != '':
                        vt_idx = int(vals[1]) - 1
                        uv = tex_coords[vt_idx]
                    else:
                        uv = [0.0, 0.0] # ダミー
                    # 配列に追加 [x, y, z, u, v]
                    final_data.extend(xyz)
                    final_data.extend(uv)

    return np.array(final_data, dtype='f4')

class UVTexture (TextureLike):
    ctx : moderngl.Context
    texture : moderngl.Texture
    def __init__(self, filepath:str) -> None:
        if static.context is None :
            raise ValueError("please execute Application.init()")
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Texture file not found: {filepath}")
        self.ctx = static.context
        surface = pygame.image.load(filepath).convert_alpha()
        surface = pygame.transform.flip(surface, False, True)
        self.texture = self.ctx.texture(
            size=surface.get_size(),
            components=4, # RGBなら3, RGBAなら4
            data=pygame.image.tobytes(surface, 'RGBA')
        )
        self.texture.filter = (moderngl.LINEAR, moderngl.LINEAR)
        self.texture.build_mipmaps()
    def use(self, location):
        self.texture.use(location=location)
    def get(self) -> moderngl.Texture:
        return self.texture
    
class UVMaterial (MaterialLike):
    program : moderngl.Program
    textures : dict[int,TextureLike]
    def __init__(self):
        if static.uv_mesh is None :
            raise ValueError("Please execute Application.init ()")
        program = static.uv_mesh.get_program()
        if program is None :
            raise ValueError("Please execute Application.init ()")
        self.program = program
        self.textures = {} # { location_index: TextureObject } の辞書

    def add_texture(self, texture:UVTexture, location:int, uniform_name:str="u_texture"):
        """
        テクスチャを登録する
        texture: Textureインスタンス
        location: 0, 1, 2...
        uniform_name: シェーダー内の変数名 ("u_texture" など)
        """
        self.textures[location] = texture

        if uniform_name in self.program:
            self.program[uniform_name] = location

    def use(self):
        """描画直前に呼ぶ：登録された全テクスチャをバインドする"""
        for loc, tex in self.textures.items():
            tex.use(location=loc)
    def get_textures(self) -> dict[int, TextureLike]:
        return self.textures
        
class UVMesh(MeshRender, MeshLike):
    ctx: moderngl.Context
    shader: ShaderContainerComponent
    material: UVMaterial
    vbo: moderngl.Buffer
    vao: moderngl.VertexArray

    def __init__(self, material: UVMaterial, mesh_data: np.ndarray) -> None:
        if static.context is None or static.uv_mesh is None:
            raise ValueError("Please execute Application.init() before creating UVMesh")

        self.ctx = static.context
        self.shader = static.uv_mesh
        self.material = material

        program = material.program
        self.vbo = self.ctx.buffer(mesh_data.astype("f4").tobytes())
        content = [(self.vbo, "3f 2f", "in_vert", "in_uv")]
        self.vao = self.ctx.vertex_array(program, content)

    def get_render_obj(self) -> tuple[moderngl.Context, moderngl.Program] | None:
        program = self.material.program
        return (self.ctx, program)

    def render(self, transform: Transform, model_matrix: np.ndarray | None = None) -> None:
        if model_matrix is None:
            model_matrix = matrix.get_i()

        self.material.use()
        self.shader.send_model(
            position=matrix.create_translation(
                transform.position.x, transform.position.y, transform.position.z
            ),
            rotation=rmatrix.create(
                transform.rotation.x, transform.rotation.y, transform.rotation.z
            ),
            scale=matrix.create_scale(
                transform.scale.x, transform.scale.y, transform.scale.z
            ),
            model_opt=model_matrix,
        )
        self.vao.render()

    def destroy(self) -> None:
        self.vao.release()
        self.vbo.release()

    def get_material(self) -> MaterialLike | None:
        return self.material