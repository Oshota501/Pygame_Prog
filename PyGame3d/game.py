import pygame
import moderngl
from PyGame3d.Scene import Scene
from PyGame3d.Scene.component import SceneComponent
import PyGame3d.matrix as matrix
from abc import ABC , abstractmethod
import PyGame3d.test as test
from PyGame3d.vector.Vector2 import Vector2
from PyGame3d.Draw.shader_container import ShaderContainer, ShaderContainerComponent,UVShaderContainer,VColorShaderContainer
import PyGame3d.static  as static 
import time

# signature : oshota , gemini AI

class ApplicationComponent(ABC) :
    @abstractmethod
    def get_scene (self) -> SceneComponent :
        pass
    @abstractmethod
    def set_scene (self,scene:SceneComponent) -> None :
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
    stage : SceneComponent
    perspective : float
    _screen : pygame.Surface | None
    fps : int|None
    _updata_time : float|None
    check_performance : bool

    def __init__(self,
            scene:Scene|None=None,
            fps:int|None=None,
            perspective:float=90,
            screen_size:tuple[int,int]=(1000,680),
            viewing_angle:float=100,
            check_performance:bool = False
    ) -> None:
        self.perspective = perspective
        self.screen_size = screen_size
        self._viewing_angle = viewing_angle
        self.ctx = None
        self._clock = pygame.time.Clock()
        self.is_init = False
        self._screen = None
        self.check_performance = check_performance
        static.uv_mesh = UVShaderContainer.open_path("./PyGame3d/shaderprogram/uvcolor.vert","./PyGame3d/shaderprogram/uvcolor.frag")
        static.vert_color_mesh = VColorShaderContainer.open_path("./PyGame3d/shaderprogram/vcolor.vert","./PyGame3d/shaderprogram/vcolor.frag")
        if static.uv_mesh is None or static.vert_color_mesh is None :
            raise ValueError("Shader program is not found.")
        self._shader_program = [
            static.uv_mesh,
            static.vert_color_mesh,
        ]
        self.fps = fps
        if fps is not None :
            self._updata_time = 1/fps
        else :
            self._updata_time = None

        if scene == None :
            self.stage = Scene()
            static.scene = self.stage
        else :
            self.stage = scene

    def get_scene(self) -> SceneComponent:
        return self.stage
    def set_scene(self,scene:SceneComponent) -> None :
        scene.start()
        self.stage = scene
    def _setup_glversion (self) :
        # OpenGLのバージョンを330に合わせます。
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, True)
        self._screen = pygame.display.set_mode(self.screen_size, pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE)
        
    def init (self) -> None :
        pygame.init()
        self._setup_glversion()
        # OpenGLコンテキストはウィンドウ作成後に生成する必要がある
        self.ctx = moderngl.create_context()
        static.context = self.ctx
        self.ctx.enable(moderngl.DEPTH_TEST|moderngl.CULL_FACE)
        if self.ctx is None:
            raise RuntimeError("\033[31mModernGL context is not initialized")

        proj_mat = matrix.create_perspective(self._viewing_angle, self.screen_size[0]/self.screen_size[1], 0.1, self.perspective)
        for prog in self._shader_program :
            prog.compile(self.ctx)
            prog.send_perspective(proj_mat)
        self.is_init = True

        return
    def set_resolution (self,resolution:tuple[int,int]) -> None :
        if self._screen is None :
            return
        print(resolution)
        self.screen_size = resolution
        proj_mat = matrix.create_perspective(self._viewing_angle, self.screen_size[0]/self.screen_size[1], 0.1, self.perspective)
        for prog in self._shader_program :
            prog.send_perspective(proj_mat)
    def start_rendering (self) :
        running = True
        if self.ctx is None or self._shader_program is None:
            print("\033[31mPlease execute init() faster than start_rendering() ")
            self.init()
            self.start_rendering()
            return
        
        test.start()
        self.get_scene().start()
        a_time = time.time()
        while running:
            no_process = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            test.update()

            self.ctx.clear(0.1, 0.1, 0.1)
            
            camera = self.get_scene().get_camera()
            for prog in self._shader_program :
                prog.send_view_by_camera(camera)
            
            now = time.time()
            deltatime = now-a_time 
            a_time = now
            if self.fps is not None :
                self._clock.tick(self.fps)
            
            if self.check_performance and self.fps is not None:
                if 1/deltatime <= self.fps*0.75 :
                    print("Warning : fps is not stabilized:", 1/deltatime)
            self.stage.update(deltatime)

            pygame.display.flip()

        pygame.quit()       
