import moderngl
import pygame
import numpy as np
from PyGame3d.GameObject.Camera import Camera
from PyGame3d.Scene.component import SceneComponent
from PyGame3d.Singleton import SingletonABCMeta
from PyGame3d.matrix import Matrix4
import os

from PyGame3d.Draw.shader_container import ShaderContainaer3dComponent, ShaderContainer, ShaderContainerComponent
from PyGame3d.Draw import MaterialLike, MeshLike, MeshRender, Transform, TextureLike

import PyGame3d.static as static
import PyGame3d.matrix as matrix
import PyGame3d.matrix.rotation as rmatrix

class UVShaderContainer (
    ShaderContainer,
    ShaderContainaer3dComponent,
    metaclass=SingletonABCMeta
) :
    def __init__(self, 
                vertpath: str = "./PyGame3d/shaderprogram/uvcolor.vert", 
                fragpath: str = "./PyGame3d/shaderprogram/uvcolor.frag"
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
            raise FileExistsError(f"ShaderProgram is not found.\n{fragpath}\n{vertpath}")
        return None
    def update(self, scene: SceneComponent) -> None:
        self.program['light_pos'].value = scene.get_light().get_position() # type: ignore # 斜め上など
        self.program['view_pos'].value = scene.get_camera().get_position()   # type: ignore # 現在のカメラ座標
        self.program['light_color'].value = scene.get_light().get_color() # type: ignore # 白色の光
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
def load_obj(filename: str) -> list[tuple[str, np.ndarray]]:
    """
    戻り値: [(マテリアル名, 頂点データ配列), (マテリアル名, 頂点データ配列), ...] のリスト
    """
    vertices = [] # v
    tex_coords = [] # vt
    normals = []    # vn
    
    # マテリアルごとにデータを蓄積する辞書
    # key: マテリアル名, value: [float, float, ...] (頂点データリスト)
    material_groups: dict[str, list[float]] = {}
    
    current_material = "default" # 初期マテリアル名
    material_groups[current_material] = [] # 初期リスト作成
    
    # MTLファイルのパス保持用
    mtl_filename = None
    base_dir = os.path.dirname(filename)

    with open(filename, 'r') as file:
        for line in file:
            parts = line.split()
            if not parts:
                continue

            # --- 基本情報の読み込み ---
            if parts[0] == 'v':
                vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
            elif parts[0] == 'vt':
                tex_coords.append([float(parts[1]), float(parts[2])])
            elif parts[0] == 'vn':
                normals.append([float(parts[1]), float(parts[2]), float(parts[3])])
            
            # --- マテリアル関連 ---
            elif parts[0] == 'mtllib':
                # MTLファイル名を記録 (後で読み込むため)
                mtl_filename = os.path.join(base_dir, parts[1])
                
            elif parts[0] == 'usemtl':
                # 使用するマテリアルを切り替える
                current_material = parts[1]
                if current_material not in material_groups:
                    material_groups[current_material] = []

            # --- 面情報の構築 ---
            elif parts[0] == 'f':
                # 現在選択されているマテリアルのリストに追加する
                vert_list = []
                for i in range(1, len(parts)):
                    vals = parts[i].split('/')
                    
                    # 座標
                    v_idx = int(vals[0]) - 1
                    xyz = vertices[v_idx]
                    
                    # UV
                    if len(vals) > 1 and vals[1] != '':
                        vt_idx = int(vals[1]) - 1
                        uv = tex_coords[vt_idx]
                    else:
                        uv = [0.0, 0.0]

                    # 法線
                    if len(vals) > 2 and vals[2] != '':
                        vn_idx = int(vals[2]) - 1
                        nm = normals[vn_idx]
                    else:
                        nm = [0.0, 1.0, 0.0]

                    # 8要素データを一時リストへ
                    vert_list.append([xyz[0],xyz[1],xyz[2], uv[0],uv[1], nm[0],nm[1],nm[2]])

                # 三角形分割して現在のマテリアルグループに追加
                if len(vert_list) >= 3 :
                    for i in range(1, len(vert_list)-1):
                        material_groups[current_material].extend(vert_list[0])
                        material_groups[current_material].extend(vert_list[i])
                        material_groups[current_material].extend(vert_list[i+1])

    # --- 解析終了後の整形 ---
    result_meshes = []
    
    # MTLファイルを解析
    mtl_data = {}
    if mtl_filename:
        mtl_data = parse_mtl(mtl_filename)
    
    # グループごとのデータを numpy 配列に変換し、MTLデータとセットで返すことも可能だが、
    # ここでは「マテリアル名」と「データ」を返し、呼び出し元で紐付けさせる
    for mat_name, data in material_groups.items():
        if len(data) > 0:
            # 配列化
            arr = np.array(data, dtype='f4')
            
            # このマテリアル名に対応するテクスチャパスなどを取得したい場合は
            # mtl_data.get(mat_name) を使うことになる
            # ここではシンプルにリストに追加して返す
            result_meshes.append({
                "material_name": mat_name,
                "data": arr,
                "mtl_info": mtl_data.get(mat_name, {}) # MTL情報も一緒に入れておく
            })
            
    return result_meshes

def parse_mtl(filename: str) -> dict:
    """
    MTLファイルを解析し、マテリアル名とプロパティの辞書を返す
    戻り値例: 
    ```py
    { 
        'MaterialA': {'map_Kd': 'textureA.png', 'Kd': [1.0, 1.0, 1.0]}, 
        'MaterialB': {'map_Kd': 'textureB.png'} 
    }
    ```
    """
    materials = {}
    current_mtl = None
    
    if not os.path.exists(filename):
        print(f"Warning: MTL file not found: {filename}")
        return {}

    with open(filename, 'r') as file:
        for line in file:
            parts = line.split()
            if not parts:
                continue
            
            # 新しいマテリアル定義
            if parts[0] == 'newmtl':
                current_mtl = parts[1]
                materials[current_mtl] = {}
            
            # 拡散反射色 (Diffuse Color)
            elif parts[0] == 'Kd':
                materials[current_mtl]['Kd'] = [float(parts[1]), float(parts[2]), float(parts[3])]
            
            # 拡散反射テクスチャ (Texture Map)
            elif parts[0] == 'map_Kd':
                materials[current_mtl]['map_Kd'] = parts[1]
                
    return materials

class UVTexture (TextureLike):
    ctx : moderngl.Context
    texture : moderngl.Texture
    def __init__(self, context:moderngl.Context,texture:moderngl.Texture) -> None:
        self.ctx = context  
        self.texture = texture
    @staticmethod
    def get_context () -> moderngl.Context :
        if static.context is None :
            raise ValueError("please execute Application.init()")
        return static.context
    def use(self, location):
        self.texture.use(location=location)
    def get(self) -> moderngl.Texture:
        return self.texture

    @classmethod
    def color(cls, color: tuple[float, float, float] | tuple[float, float, float, float], size: tuple[int, int] = (1, 1)) -> "UVTexture":
        """指定色から単色テクスチャを生成する。colorは0.0～1.0のRGBA/ RGBタプル。"""
        if static.context is None:
            raise ValueError("please execute Application.init()")
        ctx = static.context
        a = color[3] if len(color) == 4 else 1.0
        rgba8 = (
            int(max(0.0, min(1.0, color[0])) * 255),
            int(max(0.0, min(1.0, color[1])) * 255),
            int(max(0.0, min(1.0, color[2])) * 255),
            int(max(0.0, min(1.0, a)) * 255),
        )
        surface = pygame.Surface(size, flags=pygame.SRCALPHA)
        surface.fill(rgba8)
        surface = pygame.transform.flip(surface, False, True)
        tex = ctx.texture(
            size=size,
            components=4,
            data=pygame.image.tobytes(surface, "RGBA"),
        )
        tex.filter = (moderngl.LINEAR, moderngl.LINEAR)
        tex.build_mipmaps()
        inst = cls.__new__(cls)
        inst.ctx = ctx
        inst.texture = tex
        return inst
    
    @staticmethod
    def empty () -> UVTexture:
        ctx = UVTexture.get_context()
        return UVTexture(
            ctx ,
            ctx.texture(
                size=(0,0),
                components=4
            )
        )
class UVTextureImage (UVTexture,TextureLike) :
    # override
    def __init__(self, filepath: str) -> None:   
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Texture file not found: {filepath}")
        self.ctx = UVTexture.get_context()
        surface = pygame.image.load(filepath).convert_alpha()
        surface = pygame.transform.flip(surface, False, True)
        self.texture = self.ctx.texture(
            size=surface.get_size(),
            components=4, # RGBなら3, RGBAなら4
            data=pygame.image.tobytes(surface, 'RGBA')
        )
        self.texture.filter = (moderngl.LINEAR, moderngl.LINEAR)
        self.texture.build_mipmaps()

class UVMaterial (MaterialLike):
    program : moderngl.Program
    textures : dict[int,TextureLike]
    uniform_name : str
    def __init__(self):
        uv_mesh = UVShaderContainer()
        program = uv_mesh.get_program()
        if program is None :
            raise ValueError("Please execute Application.init ()")
        self.program = program
        self.textures = {} # { location_index: TextureObject } の辞書
        self.uniform_name = "u_texture"  # デフォルト値

    def add_texture(self, texture:UVTexture, location:int, uniform_name:str="u_texture"):
        """
        テクスチャを登録する
        texture: Textureインスタンス
        location: 0, 1, 2...
        uniform_name: シェーダー内の変数名 ("u_texture" など)
        """
        self.textures[location] = texture
        self.uniform_name = uniform_name
    def add_color_texture(self, color: tuple[float, float, float] | tuple[float, float, float, float], location:int=0, uniform_name:str="u_texture"):
        """単色テクスチャを登録するヘルパー。"""
        tex = UVTexture.color(color)
        self.add_texture(tex, location, uniform_name)

    def use(self):
        """描画直前に呼ぶ：登録された全テクスチャをバインドする"""
        # テクスチャをバインド
        for loc, tex in self.textures.items():
            tex.use(location=loc)
        # uniformにテクスチャユニットのインデックスを設定（最初のテクスチャを使用）
        if self.textures and self.uniform_name in self.program:
            first_location = min(self.textures.keys())
            self.program[self.uniform_name].value = first_location # type:ignore
    def get_textures(self) -> dict[int, TextureLike]:
        return self.textures
    @staticmethod
    def include_texture(texs:list[UVTexture]) -> UVMaterial:
        m = UVMaterial()
        for i,t in enumerate(texs) :
            m.add_texture(t,i)
        return m
    @staticmethod
    def img_mono_texture (filename:str) -> UVMaterial :
        tex = UVTextureImage(filepath=filename)
        return UVMaterial.include_texture([tex])

def polygone_triangle (verts:list[list[float]]) -> list[float] :
    result:list[float] = []
    if len(verts) >= 3 :
        for i in range(len(verts)-2) :
            result.extend(verts[0])
            result.extend(verts[i+1])
            result.extend(verts[i+2])
    return result
class UVSubMesh(MeshRender, MeshLike):
    ctx: moderngl.Context
    shader: UVShaderContainer
    material: UVMaterial
    vbo: moderngl.Buffer
    vao: moderngl.VertexArray

    def __init__(self, material: UVMaterial, mesh_data: np.ndarray) -> None:
        if static.context is None :
            raise ValueError("Please execute Application.init() before creating UVMesh")

        self.ctx = static.context
        self.shader = UVShaderContainer()
        self.material = material

        program = material.program
        if len(mesh_data) == 0 :
            print("Matrix cannot empty")
            mesh_data = np.array([0]*8,dtype="f4")
        self.vbo = self.ctx.buffer(mesh_data.astype("f4").tobytes())
        content = [
            # '3f 2f 3f' は floatが 3つ(vert), 2つ(uv), 3つ(norm) という意味
            (self.vbo, '3f 2f 3f', 'in_vert', 'in_uv', 'in_norm')
        ]
        self.vao = self.ctx.vertex_array(program, content)

    def get_render_obj(self) -> tuple[moderngl.Context, moderngl.Program] | None:
        program = self.material.program
        return (self.ctx, program)

    def render(self, transform: Transform, model_matrix: Matrix4 | None = None) -> None:
        if model_matrix is None:
            model_matrix = matrix.get_i()

        self.material.use()
        self.shader.send_model(
            position=matrix.create_translation(
                transform.position.x, transform.position.y, transform.position.z
            ),
            rotation=rmatrix.create(
                transform.rotation.x, transform.rotation.y, transform.rotation.z
            ),
            scale=matrix.create_scale(
                transform.scale.x, transform.scale.y, transform.scale.z
            ),
            model_opt=model_matrix,
        )
        self.vao.render()

    def destroy(self) -> None:
        self.vao.release()
        self.vbo.release()

    def get_material(self) -> MaterialLike | None:
        return self.material
    
    @staticmethod
    def load_obj (obj_filename:str) -> list[UVSubMesh] :
        objs:list[tuple[str, np.ndarray]] = load_obj(obj_filename)
        result : list[UVSubMesh] = []
        for obj in objs :
            result.append(UVSubMesh(UVMaterial.img_mono_texture(obj[0]),obj[1]))
        return result
    @staticmethod
    def cutting_boad (texture_name:str) -> UVSubMesh :
        tex = UVTextureImage(texture_name)
        material = UVMaterial()
        material.add_texture(tex,0)
        return UVSubMesh(material,np.array(
            [
                 0.5, 0.5, 0.0,  1.0, 1.0,  0.0, 0.0, 1.0,
                -0.5, 0.5, 0.0,  0.0, 1.0,  0.0, 0.0, 1.0,
                -0.5,-0.5, 0.0,  0.0, 0.0,  0.0, 0.0, 1.0,

                 0.5, 0.5, 0.0,  1.0, 1.0,  0.0, 0.0, 1.0,
                -0.5,-0.5, 0.0,  0.0, 0.0,  0.0, 0.0, 1.0,
                 0.5,-0.5, 0.0,  1.0, 0.0,  0.0, 0.0, 1.0
            ]
        ,dtype="f4"))
    @staticmethod
    def get_cube_data (texture:UVTexture) -> UVSubMesh :
        material = UVMaterial()
        material.add_texture(texture,0)
        verts:list[float] = []
        # 流石にだるすぎたのでAIにやらせた。

        # 上面 (Y+)
        verts.extend(polygone_triangle([
            [ -0.5, 0.5, -0.5, 0.0, 1.0, 0.0, 1.0, 0.0, ],
            [ -0.5, 0.5, 0.5, 0.0, 0.0, 0.0, 1.0, 0.0, ],
            [ 0.5, 0.5, 0.5, 1.0, 0.0, 0.0, 1.0, 0.0, ],
            [ 0.5, 0.5, -0.5, 1.0, 1.0, 0.0, 1.0, 0.0, ],
        ]))
        
        # 下面 (Y-)
        verts.extend(polygone_triangle([
            [ -0.5, -0.5, -0.5, 0.0, 0.0, 0.0, -1.0, 0.0, ],
            [ 0.5, -0.5, -0.5, 1.0, 0.0, 0.0, -1.0, 0.0, ],
            [ 0.5, -0.5, 0.5, 1.0, 1.0, 0.0, -1.0, 0.0, ],
            [ -0.5, -0.5, 0.5, 0.0, 1.0, 0.0, -1.0, 0.0, ],
        ]))
        
        # 前面 (Z+)
        verts.extend(polygone_triangle([
            [ -0.5, -0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 1.0, ],
            [ 0.5, -0.5, 0.5, 1.0, 0.0, 0.0, 0.0, 1.0, ],
            [ 0.5, 0.5, 0.5, 1.0, 1.0, 0.0, 0.0, 1.0, ],
            [ -0.5, 0.5, 0.5, 0.0, 1.0, 0.0, 0.0, 1.0, ],
        ]))
        
        # 背面 (Z-)
        verts.extend(polygone_triangle([
            [ -0.5, -0.5, -0.5, 1.0, 0.0, 0.0, 0.0, -1.0, ],
            [ -0.5, 0.5, -0.5, 1.0, 1.0, 0.0, 0.0, -1.0, ],
            [ 0.5, 0.5, -0.5, 0.0, 1.0, 0.0, 0.0, -1.0, ],
            [ 0.5, -0.5, -0.5, 0.0, 0.0, 0.0, 0.0, -1.0, ],
        ]))
        
        # 右面 (X+)
        verts.extend(polygone_triangle([
            [ 0.5, -0.5, -0.5, 0.0, 0.0, 1.0, 0.0, 0.0, ],
            [ 0.5, 0.5, -0.5, 0.0, 1.0, 1.0, 0.0, 0.0, ],
            [ 0.5, 0.5, 0.5, 1.0, 1.0, 1.0, 0.0, 0.0, ],
            [ 0.5, -0.5, 0.5, 1.0, 0.0, 1.0, 0.0, 0.0, ],
        ]))
        
        # 左面 (X-)
        verts.extend(polygone_triangle([
            [ -0.5, -0.5, -0.5, 1.0, 0.0, -1.0, 0.0, 0.0, ],
            [ -0.5, -0.5, 0.5, 0.0, 0.0, -1.0, 0.0, 0.0, ],
            [ -0.5, 0.5, 0.5, 0.0, 1.0, -1.0, 0.0, 0.0, ],
            [ -0.5, 0.5, -0.5, 1.0, 1.0, -1.0, 0.0, 0.0, ],
        ]))

        return UVSubMesh(material,np.array(verts,dtype="f4"))
    @staticmethod
    def floor_mesh (color=(0.6,0.6,0.6),size=(20,20)) -> UVSubMesh :
        tex = UVTexture.color(color)
        material = UVMaterial()
        material.add_texture(tex,0)

        verts = polygone_triangle([
            [-size[0]*0.5 ,0 ,-size[0]*0.5,1.0,0.0, 0.0, 1.0, 0.0],
            [-size[0]*0.5 ,0 , size[0]*0.5,1.0,0.0, 0.0, 1.0, 0.0],
            [ size[0]*0.5 ,0 , size[0]*0.5,1.0,0.0, 0.0, 1.0, 0.0],
            [ size[0]*0.5 ,0 ,-size[0]*0.5,1.0,0.0, 0.0, 1.0, 0.0],
        ])

        return UVSubMesh(material,np.array(verts,dtype="f4"))
    
class UVMesh (MeshRender, MeshLike) :
    sub_mesh : list[UVSubMesh]
    def __init__(self) -> None:
        self.sub_mesh = []
    def get_render_obj (self) -> tuple[moderngl.Context,moderngl.Program] | None :
        if len(self.sub_mesh) == 0 :
            return None
        else :
            m = self.sub_mesh[0]
            return (m.ctx,m.material.program)
    def render (self,transform:Transform, model_matrix:Matrix4|None=None) -> None:
        for sub in self.sub_mesh :
            if model_matrix is None :
                sub.render(transform,Matrix4.get_identity())
            else :
                sub.render(transform,model_matrix)
    def destroy (self) -> None:
        for sub in self.sub_mesh :
            sub.destroy()
        self.sub_mesh = []
    def get_material (self) -> MaterialLike | None :
        if len(self.sub_mesh) == 0 :
            return None
        else :
            m = self.sub_mesh[0]
            return m.get_material()

    @staticmethod
    def load_obj (filename:str) -> UVMesh :
        mesh = UVMesh()
        base_dir = os.path.dirname(filename)
        
        # 1. OBJとMTLを読み込んで分割データを取得
        sub_mesh_data_list = load_obj(filename)
        
        for item in sub_mesh_data_list:
            # pythonの辞書型は型に対する生合成がないのか？？
            mesh_data = item["data"] # type:ignore
            mtl_info:dict = item["mtl_info"] # type:ignore
            
            # 2. マテリアルを作成
            material = UVMaterial()
            
            # テクスチャ画像がある場合
            if "map_Kd" in mtl_info:
                
                texture_filename = mtl_info["map_Kd"]
                texture_path = os.path.join(base_dir, texture_filename)

                tex = UVTextureImage(texture_path)
                material.add_texture(tex, 0)
                
            else:
                # テクスチャが読み込めないだって？？
                # objファイルを直接いじるんだね
                print("\033[33mWarning\033[39m : .obj file of 3D model does not have map_Kd Option.\nWhen this option does not exsit , Texture is \".obj default color\" or pink .")
                # テクスチャがない場合は色情報(Kd)を使うか、デフォルトピンク
                color = mtl_info.get("Kd", [1.0, 0.3, 0.1])
                material.add_color_texture((color[0], color[1], color[2], 1.0))
            
            # 3. メッシュ作成
            s_mesh = UVSubMesh(material, mesh_data)
            mesh.sub_mesh.append(s_mesh)
        return mesh
