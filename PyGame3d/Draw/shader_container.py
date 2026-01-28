from moderngl import Program,Context
from PyGame3d.Scene.component import SceneComponent
from PyGame3d.matrix import Matrix4
from PyGame3d import matrix
import PyGame3d.matrix.rotation as rmatrix
from PyGame3d.matrix.lookat import create_lookAt
from PyGame3d.GameObject.Camera import Camera
from abc import ABC,abstractmethod

# signature : oshota
class ShaderContainerComponent (ABC) :
    """
    このクラスを持つ場合、metaclass=SingletonABCMeta をくっつけていないと毎回描画時にコンパイルする羽目になるので気をつけて下さい。

    """
    @abstractmethod
    def compile (self,context:Context) -> Program :
        pass
    @abstractmethod
    def get_program (self) -> Program|None :
        pass
    @abstractmethod
    def update (self,scene:SceneComponent) -> None :
        pass
class ShaderContainaer3dComponent (ABC) :
    @abstractmethod
    def send_model (self,position:Matrix4,rotation:Matrix4,scale:Matrix4,model_opt:Matrix4) -> None :
        pass
    @abstractmethod
    def send_perspective (self,projection_matrix:Matrix4) -> None :
        pass
    @abstractmethod
    def send_view (self,view_matrix:Matrix4) -> None :
        pass
    @abstractmethod
    def send_view_by_camera (self,camera:Camera) -> None :
        pass
class ShaderContainer (
    ShaderContainerComponent,
    ABC
):
    fragment : str
    vertex : str
    program : Program|None
    context : Context|None

    def __init__(self,vert:str,frag:str) -> None:
        self.vertex = vert
        self.fragment = frag
        self.program = None
        self.context = None
        return
    # コンパイラー
    def compile (self,context:Context) -> Program :
        self.context = context
        self.program = context.program(
            vertex_shader=self.vertex,
            fragment_shader=self.fragment
        )
        return self.program
    def get_render_obj(self) -> tuple[Context, Program] | None:
        if self.program is None or self.context is None :
            return None
        return (self.context,self.program)
    def get_program (self) -> Program|None :
        return self.program 
    
    def send_uniform (self,uniform_name:str,matrix:Matrix4) -> None :
        # 視野角, アスペクト比800/600, 手前0.1～奥100.0まで見える
        if self.program is None :
            print ("\033[31mShader error .\n Default vertex shader do not exist \"uniform proj\" ")
            return 
        if uniform_name in self.program :
            # 以下のignoreが気になるようでしたら、コメントアウトしているコードを使って下さい。
            self.program[uniform_name].write(matrix.tobytes()) # type: ignore
            # proj_mat_uniform = cast(moderngl.Uniform,prog['proj'])
            # proj_mat_uniform.write(proj_mat)
        else :
            print (f"\033[31mShader error .\n Default vertex shader do not exist uniform {uniform_name} ")
            return
    @abstractmethod
    def update(self, scene: SceneComponent) -> None:
        pass

