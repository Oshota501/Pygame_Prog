import numpy as np
import moderngl
import PyGame3d.matrix as matrix
import PyGame3d.matrix.rotation as rmatrix
from PyGame3d.Draw import MeshLike,MeshRender,Transform

class VertColorMesh (MeshLike,MeshRender):
    ctx : moderngl.Context
    program : moderngl.Program
    vbo : moderngl.Buffer
    vao : moderngl.VertexArray
    def __init__(self, ctx:moderngl.Context, program:moderngl.Program, vertices:np.ndarray) -> None:
        self.ctx = ctx
        self.program = program
        self.vbo = self.ctx.buffer(vertices.astype('f4').tobytes())
        content = [(self.vbo, '3f 3f', 'in_vert', 'in_color')]
        self.vao = self.ctx.vertex_array(self.program, content)
    def get_render_obj(self) -> tuple[moderngl.Context, moderngl.Program]:
        return (self.ctx,self.program)
    def render (self, transform:Transform,model_matrix:np.ndarray|None=None) -> None:
        # もし位置や回転の行列が渡されたら、シェーダーに送る
        self.program["position"].write(matrix.create_translation(transform.position.x,transform.position.y,transform.position.z)) # type: ignore
        self.program["rotation"].write(rmatrix.create(transform.rotation.x,transform.rotation.y,transform.rotation.z)) # type: ignore
        self.program["scale"].write(matrix.create_scale(transform.scale.x,transform.scale.y,transform.scale.z)) # type: ignore
        if model_matrix is not None :
            # 以下のignoreが気になるようでしたら、コメントアウトしているコードを使って下さい。
            self.program["model_opt"].write(model_matrix) # type: ignore 
            # write_prog = cast(moderngl.Uniform,self.program["model_opt"])
            # write_prog.write(model_matrix)
        
        else :
            self.program["model_opt"].write(matrix.get_i()) # type: ignore 

        # 描画実行
        self.vao.render()
    def destroy (self) -> None:
        self.vao.release()
        self.vbo.release()
    @staticmethod
    def get_cube_data(mesh_render:MeshRender) -> VertColorMesh|None:
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
        d = mesh_render.get_render_obj()
        if d is not None :
            ctx , prog = d 
            return VertColorMesh(ctx,prog,np.array(vertices, dtype='f4'))
        else : 
            return None
    @staticmethod
    def road_obj (filename:str,mesh_render:MeshRender,color=(1.0,1.0,1.0)) -> VertColorMesh|None :
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

            render = mesh_render.get_render_obj()
            if render is not None:
                ctx, prog = render
                return VertColorMesh(ctx, prog, np.array(f_vertices, dtype="f4"))
            else:
                print(f"\033[31mReading is faild : filename = {filename}")
                print("\033[31mPlease execute Application.init()")
                return None
        except Exception as e:
            print(f"\033[31mReading is faild : filename = {filename}")
            print(f"\033[31mError: {e}")
            print("\033[31mPlease check your assets name.")
            return None

    @staticmethod
    def get_checkerboad_mesh(
                mesh_render:MeshRender,
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
        
        d = mesh_render.get_render_obj()
        if d is not None :
            ctx , prog = d 
            return VertColorMesh(ctx,prog,np.array(vertices, dtype='f4'))
        else : 
            return None