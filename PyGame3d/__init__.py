import pygame
import moderngl
from PyGame3d.GameObject import ContainerComponent
from PyGame3d.Scene import SceneComponent,Scene
import PyGame3d.matrix as matrix
from PyGame3d.Draw.mesh import MeshRender
from abc import ABC , abstractmethod
import PyGame3d.test as test

class ApplicationComponent(ABC) :
    @abstractmethod
    def get_scene (self) -> SceneComponent :
        pass
    @abstractmethod
    def stage_add_child(self) -> None :
        pass

class Application (
    ApplicationComponent,
    MeshRender,
) :
    screen_size : tuple[int,int]
    ctx : moderngl.Context | None
    vertex_shader :str
    fragment_sahder :str
    clock : pygame.time.Clock
    shader_program : moderngl.Program|None
    is_init : bool

    scene : Scene
    def __init__(self) -> None:
        self.screen_size = (800,600)
        self.ctx = None
        _vertex_shader_folder = open("./PyGame3d/main.vert","r")
        _fragment_shader_folder = open("./PyGame3d/main.frag","r")
        self.vertex_shader = _vertex_shader_folder.read()
        self.fragment_sahder = _fragment_shader_folder.read()
        self.clock = pygame.time.Clock()
        self.shader_program = None
        self.is_init = False

        self.scene = Scene()

    def get_scene(self) -> SceneComponent:
        return self.scene
    def stage_add_child(self,object:ContainerComponent) -> None :
        self.scene.add_child(object)
    def get_render_obj (self) -> tuple[moderngl.Context,moderngl.Program] | None :
        if self.is_init and not self.ctx == None and not self.shader_program == None:
            return (
                self.ctx ,
                self.shader_program
            )
        else :
            print ("Please excuse Application.init()")
            return
    def setup_glversion (self) :
        # OpenGLのバージョンを330に合わせます。
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, True)
        pygame.display.set_mode(self.screen_size, pygame.OPENGL | pygame.DOUBLEBUF)
        
    def init (self) -> None :
        pygame.init()
        self.setup_glversion()
        # OpenGLコンテキストはウィンドウ作成後に生成する必要がある
        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.DEPTH_TEST|moderngl.CULL_FACE)
        if self.ctx is None:
            raise RuntimeError("ModernGL context is not initialized")
        self.shader_program = self.ctx.program(
            vertex_shader=self.vertex_shader,
            fragment_shader=self.fragment_sahder,
        )

        self.is_init = True

        # 視野角60度, アスペクト比800/600, 手前0.1～奥100.0まで見える
        proj_mat = matrix.create_perspective(60.0, self.screen_size[0]/self.screen_size[1], 0.1, 100.0)
        if 'proj' in self.shader_program:
            # 以下のignoreが気になるようでしたら、コメントアウトしているコードを使って下さい。
            self.shader_program["proj"].write(proj_mat) # type: ignore
            # proj_mat_uniform = cast(moderngl.Uniform,prog['proj'])
            # proj_mat_uniform.write(proj_mat)
        else :
            print ("Shader error .\n Default vertex shader do not exist \"uniform proj\" ")
            return
        
        test.start()
        self.get_scene().start()

        return
    
    def start_rendering (self) :
        running = True
        if self.ctx is None or self.shader_program is None:
            print("Please excuse init() faster than start_rendering() ")
            self.init()
            self.start_rendering()
            return
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            test.update()

            self.ctx.clear(0.1, 0.1, 0.1)
            view_mat = matrix.create_translation(0.0, 0.0, -3.0)
            if 'view' in self.shader_program:
                # 以下のignoreが気になるようでしたら、コメントアウトしているコードを使って下さい。
                self.shader_program['view'].write(view_mat) # type: ignore
                # view_mat_uniform = cast(moderngl.Uniform,prog['view'])
                # view_mat_uniform.write(view_mat)
            else :
                print ("Shader error .\n Default vertex shader do not exist \"uniform view\" ")
                return
            
            deltatime = self.clock.tick(60)  # ミリ秒
            self.scene.update(deltatime)

            pygame.display.flip()

        pygame.quit()       
    

    
    

    

    

    

    

    
