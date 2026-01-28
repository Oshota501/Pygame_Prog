from PyGame3d.Draw.shader_container import ShaderContainer
from PyGame3d.matrix.mat4 import Matrix4


class Mesh2dShaderContainer (
    ShaderContainer
) :
    def update(self, scene) -> None:
        # 2D描画ではカメラ(View)の影響を受けない（あるいはスクロール用のみ）
        # ここではデフォルト値をセット
        self.program['color_tint'].value = (1.0, 1.0, 1.0, 1.0) # type: ignore
        self.program['texture0'].value = 0 # type: ignore

    # 2D用の正射影行列を送るメソッド（既存のsend_perspectiveを流用しても良いが区別するため）
    def send_ortho(self, ortho_matrix: Matrix4) -> None:
        if 'proj' in self.program:
            self.program['proj'].write(ortho_matrix.tobytes()) # type: ignore
        
    @staticmethod
    def open_path (vertpath:str,fragpath:str) -> Mesh2dShaderContainer|None :
        try :
            with open(vertpath,"r") as vertshader :
                with open(fragpath,"r") as fragmentshader :
                    vert = vertshader.read()
                    frag = fragmentshader.read()
                    return Mesh2dShaderContainer(vert=vert,frag=frag)
        except :
            print("Not found shader program text file.")
        return None