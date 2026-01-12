import PyGame3d
from PyGame3d.GameObject.Cube import Cube,Sprite3D_obj_format
from PyGame3d.GameObject import Sprite3D
from PyGame3d.Scene import Scene,GameScript
from PyGame3d.vector import Vector3
import math

scene = Scene()
game = PyGame3d.Application(scene)
game.init() 

class GameObject (GameScript) :
    cube :Cube
    angle :float
    obj :Sprite3D_obj_format
    floor :Sprite3D
    def __init__(self) -> None:
        self.cube = Cube(game)
        self.angle = 0.0
        self.obj = Sprite3D_obj_format(game,"./Assets/test.obj")
        self.floor = Sprite3D()
        from PyGame3d.Draw.vcolormesh import VertColorMesh
        self.floor.mesh = VertColorMesh.get_checkerboad_mesh(game,color1=(0.0,0.5,0.0),color2=(0.01,0.01,0.01))
    def start(self) -> None:
        game.stage_add_child(self.cube)
        self.obj.scale *= 0.2
        game.stage_add_child(self.obj)
        self.floor.position.y = -3 
        game.stage_add_child(self.floor)
    def update(self, delta_MS: float) -> None :
        self.angle += 0.001*delta_MS
        self.cube.add_rotation(Vector3(math.sin(self.angle),math.cos(self.angle),math.sin(self.angle)))
        game.scene.camera.position = Vector3(math.cos(self.angle)*5,0.0,math.sin(self.angle)*5)
        game.scene.camera.look_at(self.cube.position)

scene.script_add(GameObject())
game.start_rendering()