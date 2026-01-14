import pygame
import moderngl
from PyGame3d.GameObject import ContainerComponent
from PyGame3d.Scene import SceneComponent,Scene
import PyGame3d.matrix as matrix
from abc import ABC , abstractmethod
import PyGame3d.test as test
from PyGame3d.vector.Vector2 import Vector2
from PyGame3d.Draw.shader_container import ShaderContainer, ShaderContainerComponent
import PyGame3d.static  as static 

class ApplicationComponent(ABC) :
    @abstractmethod
    def get_scene (self) -> SceneComponent :
        pass

    

class Application (
    ApplicationComponent
) :
    screen_size : tuple[int,int]
    _viewing_angle : float

    ctx : moderngl.Context | None
    _clock : pygame.time.Clock
    is_init : bool
    _shader_program : list[ShaderContainerComponent]
    stage : Scene

    def __init__(self,scene:Scene|None=None) -> None:
        self.screen_size = (800,600)
        self._viewing_angle = 100.0 
        self.ctx = None
        self._clock = pygame.time.Clock()
        self.is_init = False
        static.uv_mesh = ShaderContainer.open_path("./PyGame3d/shaderprogram/uvcolor.vert","./PyGame3d/shaderprogram/uvcolor.frag")
        static.vert_color_mesh = ShaderContainer.open_path("./PyGame3d/shaderprogram/vcolor.vert","./PyGame3d/shaderprogram/vcolor.frag")
        if static.uv_mesh is None or static.vert_color_mesh is None :
            raise ValueError("Shader program is not found.")
        self._shader_program = [
            static.uv_mesh,
            static.vert_color_mesh,
        ]

        if scene == None :
            self.stage = Scene()
            static.scene = self.stage
        else :
            self.stage = scene

    def get_scene(self) -> SceneComponent:
        return self.stage
    def _setup_glversion (self) :
        # OpenGLのバージョンを330に合わせます。
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, True)
        pygame.display.set_mode(self.screen_size, pygame.OPENGL | pygame.DOUBLEBUF)
        
    def init (self) -> None :
        pygame.init()
        self._setup_glversion()
        # OpenGLコンテキストはウィンドウ作成後に生成する必要がある
        self.ctx = moderngl.create_context()
        static.context = self.ctx
        self.ctx.enable(moderngl.DEPTH_TEST|moderngl.CULL_FACE)
        if self.ctx is None:
            raise RuntimeError("\033[31mModernGL context is not initialized")

        proj_mat = matrix.create_perspective(self._viewing_angle, self.screen_size[0]/self.screen_size[1], 0.1, 100.0)
        for prog in self._shader_program :
            prog.compile(self.ctx)
            prog.send_perspective(proj_mat)
        self.is_init = True

        return
    
    def start_rendering (self) :
        running = True
        if self.ctx is None or self._shader_program is None:
            print("\033[31mPlease execute init() faster than start_rendering() ")
            self.init()
            self.start_rendering()
            return
        
        test.start()
        self.get_scene().start()

        while running:
            evs = self.stage.get_event_listener()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                for ev in evs :
                    if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP :
                        ev.event_happen(Vector2(event.pos))
                    elif event.type == ev.event_type :
                        ev.event_happen(Vector2())

            test.update()

            self.ctx.clear(0.1, 0.1, 0.1)
            
            camera = self.get_scene().get_camera()
            for prog in self._shader_program :
                prog.send_view_by_camera(camera)
            
            deltatime = self._clock.tick(60)  # ミリ秒
            self.stage.update(deltatime)

            pygame.display.flip()

        pygame.quit()       
