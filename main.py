import pygame
import moderngl
import numpy as np
import math
from typing import cast

# X軸周りの回転行列を作る関数
def create_rotation_matrix_x(degrees):
    rad = math.radians(degrees)
    c = math.cos(rad)
    s = math.sin(rad)
    # 4x4行列 (列優先)
    return np.array([
        [1.0, 0.0, 0.0, 0.0],
        [0.0,   c,   s, 0.0],
        [0.0,  -s,   c, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ], dtype='f4')

# Y軸周りの回転行列を作る関数
def create_rotation_matrix_y(degrees):
    rad = math.radians(degrees)
    c = math.cos(rad)
    s = math.sin(rad)
    return np.array([
        [  c, 0.0,  -s, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [  s, 0.0,   c, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ], dtype='f4')

# OpenGLのバージョンを330に合わせます。
pygame.init()
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, True)
pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)

# ModernGLのコンテキストを作成
ctx = moderngl.create_context()

# シェーダーを読み込みます。
_vertex_shader_folder = open("./main.vert","r")
_fragment_shader_folder = open("./main.frag","r")
vertex_shader = _vertex_shader_folder.read()
fragment_sahder = _fragment_shader_folder.read()

prog = ctx.program(
    vertex_shader=vertex_shader,
    fragment_shader=fragment_sahder,
)

# ポリゴン
# X, Y, Z, R, G, B の順でデータを並べる
vertices = np.array([
    # 頂点座標(x,y,z)   # 色(r,g,b)
     0.0,  0.5, 0.0,    1.0, 0.0, 0.0, # 上 (赤)
    -0.5, -0.5, 0.0,    0.0, 1.0, 0.0, # 左下 (緑)
     0.5, -0.5, 0.0,    0.0, 0.0, 1.0, # 右下 (青)
], dtype='f4')

# VBO (Vertex Buffer Object): GPUのメモリにデータを転送
vbo = ctx.buffer(vertices.tobytes())

# VAO (Vertex Array Object): シェーダーの変数とデータの対応付け
vao = ctx.simple_vertex_array(prog, vbo, 'in_vert', 'in_color')

clock = pygame.time.Clock()
angle = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 画面を灰色でクリア
    ctx.clear(0.1, 0.1, 0.1)

    # 角度を更新
    angle += 1
    
    # 行列を作成してシェーダーに送信 (uniform変数 'rotation' に書き込む)
    # ここでY軸回転行列を作っているので、くるくる回る
    rot_mat = create_rotation_matrix_y(angle)
    
    u_rotation = cast(moderngl.Uniform, prog['rotation'])
    u_rotation.write(rot_mat)

    # 描画実行
    vao.render()

    # 画面更新
    pygame.display.flip()
    clock.tick(60)

pygame.quit()