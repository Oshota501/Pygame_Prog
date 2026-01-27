import numpy as np
from PyGame3d.Draw.uvmesh import UVMaterial, UVSubMesh
from PyGame3d.vector import Vector3

# signature : oshota
class CreativeUVMesh (UVSubMesh) :
    vert : list[Vector3]
    uv : list[tuple[float,float]]
    mesh_data : list[float]
    def __init__(self, material: UVMaterial) -> None:
        super().__init__(material, np.array([],dtype="f4"))
        self.mesh_data = []
        self.vert = []
        self.uv = []
    def add_vert (self,vert:Vector3,uv:tuple[float,float]) -> int :
        """indexを返します。（頂点IDとなります。）"""
        self.vert.append(vert)
        self.uv.append(uv)
        return len(self.vert)-1
    def add_surface_polygon3v (self,vertex_id:tuple[int,int,int]) -> None :
        for vi in vertex_id : 
            self.mesh_data.extend(self.vert[vi])
            uv = self.uv[vi]
            self.mesh_data.append(uv[0])
            self.mesh_data.append(uv[1])
    def set_polygon (self,vertex_id:list[int]) -> None :
        for id in range(1,len(vertex_id)-1) :
            self.add_surface_polygon3v((vertex_id[0],vertex_id[id],vertex_id[id+1]))
    def set_squarea (self,size:Vector3=Vector3(1,1,1)) -> None :
        surface:Vector3=Vector3(1,1,0)
        v0 = self.add_vert(surface*size*Vector3(1,1,0),(0,1))
        v1 = self.add_vert(surface*size*Vector3(1,-1,0),(0,0))
        v2 = self.add_vert(surface*size*Vector3(-1,-1,0),(1,0))
        v3 = self.add_vert(surface*size*Vector3(-1,1,0),(1,1))
        self.set_polygon([v0,v1,v2,v3])
    def create (self) -> None :
        program = self.material.program
        if len(self.mesh_data ) == 0 :
            print("send buffur is empty")
            return
        self.vbo = self.ctx.buffer(np.array(self.mesh_data,dtype="f4").astype("f4").tobytes())
        content = [(self.vbo, "3f 2f", "in_vert", "in_uv")]
        self.vao = self.ctx.vertex_array(program, content)