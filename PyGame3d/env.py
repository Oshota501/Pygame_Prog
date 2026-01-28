from PyGame3d.Draw.mesh2d import Mesh2dShaderContainer
from PyGame3d.Draw.uvmesh import UVShaderContainer
from PyGame3d.Draw.vcolormesh import VColorShaderContainer
DEFAULT_SHADERS = [
    UVShaderContainer() ,
    VColorShaderContainer() ,
    Mesh2dShaderContainer ()
]
DEFAULT_3D_SHADERS = [
    UVShaderContainer() ,
    VColorShaderContainer() ,
]