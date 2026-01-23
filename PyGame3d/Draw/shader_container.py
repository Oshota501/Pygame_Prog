from moderngl import Program,Context
import numpy as np
from PyGame3d import matrix
import PyGame3d.matrix.rotation as rmatrix
from PyGame3d.matrix.lookat import create_lookAt
from PyGame3d.GameObject.Camera import Camera
from abc import ABC,abstractmethod

# signature : oshota
class ShaderContainerComponent (ABC) :
    @abstractmethod
    def compile (self,context:Context) -> Program :
        pass
    @abstractmethod
    def get_program (self) -> Program|None :
        pass
    @abstractmethod
    def send_model (self,position:np.ndarray,rotation:np.ndarray,scale:np.ndarray,model_opt:np.ndarray) -> None :
        pass
    @abstractmethod
    def send_perspective (self,projection_matrix:np.ndarray) -> None :
        pass
    @abstractmethod
    def send_view (self,view_matrix:np.ndarray) -> None :
        pass
    @abstractmethod
    def send_view_by_camera (self,camera:Camera) -> None :
        pass

class ShaderContainer (
    ShaderContainerComponent,
):
    fragment : str
    vertex : str
    program : Program

    def __init__(self,vert:str,frag:str) -> None:
        self.vertex = vert
        self.fragment = frag
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
    
    def send_uniform (self,uniform_name:str,matrix:np.ndarray) -> None :
        # 視野角, アスペクト比800/600, 手前0.1～奥100.0まで見える
        if self.program is None :
            print ("\033[31mShader error .\n Default vertex shader do not exist \"uniform proj\" ")
            return 
        if uniform_name in self.program :
            # 以下のignoreが気になるようでしたら、コメントアウトしているコードを使って下さい。
            self.program[uniform_name].write(matrix) # type: ignore
            # proj_mat_uniform = cast(moderngl.Uniform,prog['proj'])
            # proj_mat_uniform.write(proj_mat)
        else :
            print (f"\033[31mShader error .\n Default vertex shader do not exist uniform {uniform_name} ")
            return
    def send_model (self,position:np.ndarray,rotation:np.ndarray,scale:np.ndarray,model_opt:np.ndarray) -> None :
        self.send_uniform("position",position)
        self.send_uniform("rotation",rotation)
        self.send_uniform("scale",scale)
        self.send_uniform("model_opt",model_opt)
        return
    def send_perspective (self,projection_matrix:np.ndarray) -> None :
        self.send_uniform("proj",projection_matrix)
        return
    def send_view (self,view_matrix:np.ndarray) -> None :
        self.send_uniform("view",view_matrix) 
        return
    def send_view_by_camera (self,camera:Camera) -> None :
        view_mat:np.ndarray
        # 注意 カメラ行列はマイナスをかける。
        c = camera.get_position()
        cr = camera.get_rotation()
        trans_mat = matrix.create_translation(-c.x,-c.y,-c.z)
        rot_mat = rmatrix.create_camera(-cr.x,-cr.y,-cr.z)
        view_mat = ( trans_mat @ rot_mat )
        self.send_uniform("view",view_mat)
        return

    @staticmethod
    def open_path (vertpath:str,fragpath:str) -> ShaderContainer|None :
        try :
            with open(vertpath,"r") as vertshader :
                with open(fragpath,"r") as fragmentshader :
                    vert = vertshader.read()
                    frag = fragmentshader.read()
                    return ShaderContainer(vert=vert,frag=frag)
        except :
            print("Not found shader program text file.")
        return None
