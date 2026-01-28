import numpy as np
import moderngl
from PyGame3d.GameObject.Camera import Camera
from PyGame3d.Scene.component import SceneComponent
from PyGame3d.Singleton import SingletonABCMeta
import PyGame3d.matrix as matrix
import PyGame3d.matrix.rotation as rmatrix
from PyGame3d.Draw import MaterialLike, MeshLike,MeshRender,Transform
from PyGame3d.Draw.shader_container import ShaderContainaer3dComponent, ShaderContainer, ShaderContainerComponent
import PyGame3d.static as static
from PyGame3d.matrix import Matrix4

class VColorShaderContainer (
    ShaderContainer,
    ShaderContainaer3dComponent,
    metaclass=SingletonABCMeta
) :
    def __init__(self,
                vertpath: str = "./PyGame3d/shaderprogram/vcolor.vert", 
                fragpath: str = "./PyGame3d/shaderprogram/vcolor.frag", 
    ) -> None:
        try :
            vert : str
            frag : str
            with open(vertpath,"r") as vertshader :
                with open(fragpath,"r") as fragmentshader :
                    vert = vertshader.read()
                    frag = fragmentshader.read()
            super().__init__(vert, frag)
        except :
            print("Not found shader program text file.")

    def update(self, scene: SceneComponent) -> None:
        return
    def send_model (self,position:Matrix4,rotation:Matrix4,scale:Matrix4,model_opt:Matrix4) -> None :
        self.send_uniform("position",position)
        self.send_uniform("rotation",rotation)
        self.send_uniform("scale",scale)
        self.send_uniform("model_opt",model_opt)
        return
    def send_perspective (self,projection_matrix:Matrix4) -> None :
        self.send_uniform("proj",projection_matrix)
        return
    def send_view (self,view_matrix:Matrix4) -> None :
        self.send_uniform("view",view_matrix) 
        return
    def send_view_by_camera (self,camera:Camera) -> None :
        view_mat:Matrix4
        # 注意 カメラ行列はマイナスをかける。
        c = camera.get_position()
        cr = camera.get_rotation()
        trans_mat = matrix.create_translation(-c.x,-c.y,-c.z)
        rot_mat = rmatrix.create_camera(-cr.x,-cr.y,-cr.z)
        view_mat = ( trans_mat * rot_mat )
        self.send_uniform("view",view_mat)
        return

# signature : Gemini AI
class VertColorMesh (MeshLike,MeshRender):
    rend : VColorShaderContainer
    vbo : moderngl.Buffer
    vao : moderngl.VertexArray
    ctx : moderngl.Context

    def __init__(self, vertices:np.ndarray) -> None:
        if static.context is None :
            raise
        self.ctx = static.context
        self.rend = VColorShaderContainer()
        program = self.rend.get_program()
        if self.ctx is None or program is None :
            print("error : Read shader has probrem .")
            raise 
        else :
            self.vbo = self.ctx.buffer(vertices.astype('f4').tobytes())
            content = [(self.vbo, '3f 3f', 'in_vert', 'in_color')]
            self.vao = self.ctx.vertex_array(program, content)
    def get_render_obj(self) -> ShaderContainerComponent:
        return self.rend
    def render (self, transform:Transform,model_matrix:Matrix4=matrix.get_i()) -> None:
        # もし位置や回転の行列が渡されたら、シェーダーに送る
        self.rend.send_model(
            position = matrix.create_translation(transform.position.x,transform.position.y,transform.position.z) ,
            rotation = rmatrix.create(transform.rotation.x,transform.rotation.y,transform.rotation.z) ,
            scale = matrix.create_scale(transform.scale.x,transform.scale.y,transform.scale.z) ,
            model_opt = model_matrix
        )
        self.vao.render()
    def destroy (self) -> None:
        self.vao.release()
        self.vbo.release()
    def get_material(self) -> MaterialLike | None:
        return None
    @staticmethod
    def get_cube_data(ctx:moderngl.Context,shader:ShaderContainerComponent) -> VertColorMesh:
        vertices = [
            # 前面 (z = 0.5) - 赤
            -0.5, -0.5,  0.5, 1.0, 0.0, 0.0,
             0.5, -0.5,  0.5, 1.0, 0.0, 0.0,
             0.5,  0.5,  0.5, 1.0, 0.0, 0.0,
            -0.5, -0.5,  0.5, 1.0, 0.0, 0.0,
             0.5,  0.5,  0.5, 1.0, 0.0, 0.0,
            -0.5,  0.5,  0.5, 1.0, 0.0, 0.0,
            
            # 背面 (z = -0.5) - 緑
             0.5, -0.5, -0.5, 0.0, 1.0, 0.0,
            -0.5, -0.5, -0.5, 0.0, 1.0, 0.0,
            -0.5,  0.5, -0.5, 0.0, 1.0, 0.0,
             0.5, -0.5, -0.5, 0.0, 1.0, 0.0,
            -0.5,  0.5, -0.5, 0.0, 1.0, 0.0,
             0.5,  0.5, -0.5, 0.0, 1.0, 0.0,
            
            # 右面 (x = 0.5) - 青
             0.5, -0.5,  0.5, 0.0, 0.0, 1.0,
             0.5, -0.5, -0.5, 0.0, 0.0, 1.0,
             0.5,  0.5, -0.5, 0.0, 0.0, 1.0,
             0.5, -0.5,  0.5, 0.0, 0.0, 1.0,
             0.5,  0.5, -0.5, 0.0, 0.0, 1.0,
             0.5,  0.5,  0.5, 0.0, 0.0, 1.0,
            
            # 左面 (x = -0.5) - 黄
            -0.5, -0.5, -0.5, 1.0, 1.0, 0.0,
            -0.5, -0.5,  0.5, 1.0, 1.0, 0.0,
            -0.5,  0.5,  0.5, 1.0, 1.0, 0.0,
            -0.5, -0.5, -0.5, 1.0, 1.0, 0.0,
            -0.5,  0.5,  0.5, 1.0, 1.0, 0.0,
            -0.5,  0.5, -0.5, 1.0, 1.0, 0.0,
            
            # 上面 (y = 0.5) - マゼンタ
            -0.5,  0.5,  0.5, 1.0, 0.0, 1.0,
             0.5,  0.5,  0.5, 1.0, 0.0, 1.0,
             0.5,  0.5, -0.5, 1.0, 0.0, 1.0,
            -0.5,  0.5,  0.5, 1.0, 0.0, 1.0,
             0.5,  0.5, -0.5, 1.0, 0.0, 1.0,
            -0.5,  0.5, -0.5, 1.0, 0.0, 1.0,
            
            # 下面 (y = -0.5) - シアン
            -0.5, -0.5, -0.5, 0.0, 1.0, 1.0,
             0.5, -0.5, -0.5, 0.0, 1.0, 1.0,
             0.5, -0.5,  0.5, 0.0, 1.0, 1.0,
            -0.5, -0.5, -0.5, 0.0, 1.0, 1.0,
             0.5, -0.5,  0.5, 0.0, 1.0, 1.0,
            -0.5, -0.5,  0.5, 0.0, 1.0, 1.0,
        ]

        return VertColorMesh(np.array(vertices, dtype='f4'))

    @staticmethod
    def road_obj (ctx:moderngl.Context,shader:ShaderContainerComponent,filename:str,color=(1.0,1.0,1.0)) -> VertColorMesh|None:
        vertices : list[tuple[float,float,float]] = []
        tex_coords = [] # vt
        indices : list[int] = []
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    parts = line.split()
                    if not parts:
                        continue
                    if parts[0] == 'v':
                        vertices.append((float(parts[1]), float(parts[2]), float(parts[3])))
                    elif parts[0] == 'vt' :
                        tex_coords.append([float(parts[1]), float(parts[2])])
                    elif parts[0] == 'f':
                        # OBJは1始まりかつ四角面があるので、三角形ファンで分割しつつ0始まりに補正
                        face_idx: list[int] = []
                        for token in parts[1:]:
                            index_str = token.split('/')[0]
                            if index_str:
                                face_idx.append(int(index_str) - 1)
                        if len(face_idx) >= 3:
                            for i in range(1, len(face_idx) - 1):
                                indices.extend([face_idx[0], face_idx[i], face_idx[i + 1]])

            f_vertices: list[float] = []
            for index in indices:
                if 0 <= index < len(vertices):
                    f_vertices.extend(vertices[index])
                    f_vertices.extend([color[0], color[1], color[2]])
                else:
                    raise IndexError(f"Index {index} out of bounds for vertices of length {len(vertices)}")


            return VertColorMesh(np.array(f_vertices, dtype="f4"))
        except Exception as e:
            print(f"\033[31mReading is faild : filename = {filename}")
            print(f"\033[31mError: {e}")
            print("\033[31mPlease check your assets name.")
            return None

    @staticmethod
    def get_checkerboad_mesh(
                ctx:moderngl.Context,
                shader:ShaderContainerComponent,
                grid_size = 40 ,
                tile_size = 0.4 ,
                color1 = (1.0,1.0,1.0) ,
                color2 = (0.0,0.0,0.0) ,
    ) -> VertColorMesh|None:
        vertices = []
        
        start_x = -grid_size * tile_size *0.5
        start_z = -grid_size * tile_size *0.5
        
        # グリッドを生成
        for i in range(grid_size):
            for j in range(grid_size):
                # タイルの左下コーナー位置
                x0 = start_x + i * tile_size
                z0 = start_z + j * tile_size
                x1 = x0 + tile_size
                z1 = z0 + tile_size
                
                # チェッカーボード模様：色を決定
                # (i + j) % 2 で白黒を交互に配置
                if (i + j) % 2 == 0:
                    color = color1  # default 白
                else:
                    color = color2  # default 黒
                
                # タイルを2つの三角形で構成（反時計回り）
                # 1つ目の三角形（左下→左上→右上）
                vertices.extend([
                    x0, 0.0, z0, color[0], color[1], color[2],
                    x0, 0.0, z1, color[0], color[1], color[2],
                    x1, 0.0, z1, color[0], color[1], color[2],
                ])
                
                # 2つ目の三角形（左下→右上→右下）
                vertices.extend([
                    x0, 0.0, z0, color[0], color[1], color[2],
                    x1, 0.0, z1, color[0], color[1], color[2],
                    x1, 0.0, z0, color[0], color[1], color[2],
                ])
        

        return VertColorMesh(np.array(vertices, dtype='f4'))
