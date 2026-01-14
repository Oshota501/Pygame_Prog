import moderngl
from PyGame3d import Scene
from PyGame3d.Draw.shader_container import ShaderContainerComponent


context : moderngl.Context | None = None
vert_color_mesh : ShaderContainerComponent | None = None
uv_mesh : ShaderContainerComponent | None = None

scene : Scene | None = None
