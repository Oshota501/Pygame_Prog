import pygame
import moderngl
import numpy as np
import matrix.rotation
from Draw.mesh import Mesh
from typing import cast
import math
import PyGame3d.test as test
import PyGame3d.env as env

from GameObject.gameobject import BaseGameObject

screen = BaseGameObject()

def init() -> None:
    # OpenGLのバージョンを330に合わせます。
    pygame.init()
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, True)
    pygame.display.set_mode(env.SCREEN, pygame.OPENGL | pygame.DOUBLEBUF)

    # ModernGLのコンテキストを作成
    ctx = moderngl.create_context()
    ctx.enable(moderngl.DEPTH_TEST|moderngl.CULL_FACE)
    # シェーダーを読み込みます。
    _vertex_shader_folder = open("./main.vert","r")
    _fragment_shader_folder = open("./main.frag","r")
    vertex_shader = _vertex_shader_folder.read()
    fragment_sahder = _fragment_shader_folder.read()

    prog = ctx.program(
        vertex_shader=vertex_shader,
        fragment_shader=fragment_sahder,
    )

    clock = pygame.time.Clock()
    angle = 0

    cube_data = Mesh.get_cube_data()
    my_cube = Mesh(ctx, prog, cube_data)

    # 視野角60度, アスペクト比800/600, 手前0.1～奥100.0まで見える
    proj_mat = matrix.create_perspective(60.0, env.SCREEN[0]/env.SCREEN[1], 0.1, 100.0)

    if 'proj' in prog:
        # 以下のignoreが気になるようでしたら、コメントアウトしているコードを使って下さい。
        prog["proj"].write(proj_mat) # type: ignore
        # proj_mat_uniform = cast(moderngl.Uniform,prog['proj'])
        # proj_mat_uniform.write(proj_mat)
    else :
        print ("Shader error .\n Default vertex shader do not exist \"uniform proj\" ")
        return
    
    running = True
    test.start()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        test.updata()

        ctx.clear(0.1, 0.1, 0.1)
        view_mat = matrix.create_translation(0.0, 0.0, -3.0)
        if 'view' in prog:
            # 以下のignoreが気になるようでしたら、コメントアウトしているコードを使って下さい。
            prog['view'].write(view_mat) # type: ignore
            # view_mat_uniform = cast(moderngl.Uniform,prog['view'])
            # view_mat_uniform.write(view_mat)
        else :
            print ("Shader error .\n Default vertex shader do not exist \"uniform view\" ")
            return
        
        deltatime = clock.tick(60) / 1000.0  # ミリ秒を秒に変換

        angle += 1
        
        model_mat = matrix.rotation.create(angle,angle,angle) @ matrix.create_translation(math.sin(angle/100),math.cos(angle/100),0.0)
        my_cube.render(model_matrix=model_mat)

        pygame.display.flip()

    pygame.quit()