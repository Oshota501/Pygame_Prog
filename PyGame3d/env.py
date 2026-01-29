from PyGame3d.Draw.mesh2d import Mesh2dShaderContainer
from PyGame3d.Draw.uvmesh import UV3dShaderContainer
from PyGame3d.Draw.vcolormesh import VColorShaderContainer
DEFAULT_SHADERS = [
    UV3dShaderContainer() ,
    VColorShaderContainer() ,
    Mesh2dShaderContainer ()
]
DEFAULT_3D_SHADERS = [
    UV3dShaderContainer() ,
    VColorShaderContainer() ,
]