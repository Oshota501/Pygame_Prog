import numpy as np
import moderngl
from typing import cast
from PyGame3d.vector.Vector3 import Vector3
from abc import ABC , abstractmethod
import PyGame3d.matrix as matrix
import PyGame3d.matrix.rotation as rmatrix

from dataclasses import dataclass

@dataclass
class Transform :
    position: Vector3
    rotation: Vector3
    scale: Vector3

class MeshRender (ABC) :
    @abstractmethod
    def get_render_obj (self) -> tuple[moderngl.Context,moderngl.Program] | None :
        pass 

class MeshLike (ABC) :
    @abstractmethod
    def render (self,transform:Transform, model_matrix=None) -> None:
        pass
    @abstractmethod
    def destroy (self) -> None:
        pass

class Mesh (MeshLike,MeshRender):
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
    def get_cube_data(mesh_render:MeshRender) -> Mesh|None:
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
            return Mesh(ctx,prog,np.array(vertices, dtype='f4'))
        else : 
            return None
    @staticmethod
    def road_obj (filename:str,mesh_render:MeshRender,color=(1.0,1.0,1.0)) -> Mesh|None :
        vertices : list[tuple[float,float,float]] = []
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
                return Mesh(ctx, prog, np.array(f_vertices, dtype="f4"))
            else:
                print(f"\033[31mReading is faild : filename = {filename}")
                print("\033[31mPlease execute Application.init()")
                return None
        except Exception as e:
            print(f"\033[31mReading is faild : filename = {filename}")
            print(f"\033[31mError: {e}")
            print("\033[31mPlease check your assets name.")
            return None
