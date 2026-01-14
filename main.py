import PyGame3d
from PyGame3d.GameObject.Cube import Cube,Floor,CuttingBoad
from PyGame3d.GameObject.obj import UVColorMesh_Sprite3D
from PyGame3d.Scene import Scene,GameScript
from PyGame3d.vector import Vector3
import math

scene = Scene()
game = PyGame3d.Application(scene)
game.init() 

class GameObject (GameScript) :
    # cube :Cube
    # angle :float
    # floor :Floor
    useTextureObj :UVColorMesh_Sprite3D

    def __init__(self) -> None:
        self.cube = Cube()
        self.angle = 0.0
        self.floor = Floor()
        self.useTextureObj = UVColorMesh_Sprite3D("./Assets/tex.png","./Assets/u.obj")
        self.cutting = CuttingBoad("./Assets/tex.png")
    def start(self) -> None:
        game.stage.add_child(self.cube)
        self.floor.position.y = -3 
        game.stage.add_child(self.floor)
        self.useTextureObj.position += Vector3(0,3,0)
        self.useTextureObj.scale *= Vector3(0.2,0.2,0.2)
        game.stage.add_child(self.useTextureObj)
        self.cutting.position -= Vector3(0,0,6)
        self.cutting.scale = Vector3(10,10,10)
        game.stage.add_child(self.cutting)
    def update(self, delta_MS: float) -> None :
        self.angle += 0.001*delta_MS
        self.cutting.rotation.z += self.angle
        self.cube.add_rotation(Vector3(math.sin(self.angle),math.cos(self.angle),math.sin(self.angle)))
        game.stage.camera.position = Vector3(math.cos(self.angle)*5,0.0,math.sin(self.angle)*5)
        game.stage.camera.look_at(self.cube.position-Vector3(0,0,0))

scene.script_add(GameObject())
game.start_rendering()