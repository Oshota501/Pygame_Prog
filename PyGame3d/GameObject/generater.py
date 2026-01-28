from PyGame3d.vector import Vector2, Vector3
from PyGame3d.GameObject.Sample import Cube, Floor
from PyGame3d.Scene import Scene

from PyGame3d.GameObject.ui_2d import UI_2d

class DefaultObjectGenerater :
    resolution : tuple[int,int]
    stage : Scene
    def __init__(self,
                resolution : tuple[int,int] ,
                stage : Scene
    ) -> None:
        self.resolution = resolution
        self.stage = stage
    
    def cube (self,
            position:tuple[float,float,float]|Vector3=(0.0,0.0,0.0),
            rotation:tuple[float,float,float]|Vector3=(0.0,0.0,1.0),
            scale:tuple[float,float,float]|Vector3=(1.0,1.0,1.0),
            velocity_enabled:bool = False,
            velocity:tuple[float,float,float]|Vector3=(0.0,0.0,0.0),
            coefficient:float=0.5 ,
            collide_enabled:bool = False,
    ) -> Cube :
        cube = Cube.transform(
            Vector3(*position),
            Vector3(*rotation),
            Vector3(*scale)
        )
        cube.set_collide_enabled(collide_enabled)
        cube.set_collide_enabled(velocity_enabled)
        cube.set_velocity(Vector3(*velocity))
        cube.physics.coefficient=coefficient
        self.stage.add_child(cube)
        return cube
    def floor (self,
            position:tuple[float,float,float]|Vector3=(0.0,-3.0,0.0),
            rotation:tuple[float,float,float]|Vector3=(0.0,0.0,0.0),
            scale:tuple[float,float,float]|Vector3=(1.0,1.0,1.0),
    ) -> Floor :
        floor = Floor.transform(
            position=Vector3(*position),
            rotation=Vector3(*rotation),
            scale=Vector3(*scale),
        )
        return floor
    def get_ui_center (self) -> tuple[int,int] :
        return (
            int(self.resolution[0] * 0.5 ),
            int(self.resolution[1] * 0.5 )
        )
    def ui_text (self,
                text:str,
                font_path:str,
                color:tuple[int,int,int]=(255,255,255),
                font_size:int = 24,
                text_pivod:bool = True,
                position:tuple[int,int]|Vector2 = (20,20)
    ) -> UI_2d :
        from PyGame3d.Draw.mesh2d import Mesh2d
        mesh = Mesh2d.text(text,font_path=font_path,color=color,font_size=font_size,text_pivod=text_pivod)
        ui = UI_2d(mesh,resolution=self.resolution)
        ui.position = Vector3(position[0],position[1],0)
        return ui
