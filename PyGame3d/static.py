import moderngl
from PyGame3d.Scene import Scene
from PyGame3d.vector import Vector3


context : moderngl.Context | None = None

scene : Scene | None = None

gravity_asseleration : Vector3 = Vector3(0,-9.80665,0)
