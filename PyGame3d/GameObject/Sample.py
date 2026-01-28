import math
from PyGame3d.Draw import MeshLike
from PyGame3d.GameObject.Collide import AxisAlignedBoundingBox, SimpleBoundingObject
from PyGame3d.GameObject.sprite import Sprite3D, Sprite3DBoundingObject, Sprite3DPhysicsComponent
from PyGame3d.Draw.vcolormesh import VColorShaderContainer, VertColorMesh
from PyGame3d.Draw.uvmesh import UVSubMesh,UVTexture
import PyGame3d.static as static
from PyGame3d.vector import Vector2, Vector3
import pygame

# signature : oshota
class Cube (Sprite3D) :
    def __init__(self) -> None:
        super().__init__()
        
        self.mesh = UVSubMesh.get_cube_data(UVTexture.color((0.3,0.3,0.3)))

        self.set_bounding_obj(Vector3(-0.5,-0.5,-0.5),Vector3(0.5,0.5,0.5))
    @staticmethod
    def transform (
            position=Vector3(0,0,0),
            rotation=Vector3(0,0,1),
            scale=Vector3(1,1,1)
    )-> Cube :
        f = Cube()
        f.set_position(position)
        f.set_rotation(rotation)
        f.set_scale(scale)
        return f
class VColorCube (Sprite3D) :
    def __init__(self) -> None:
        super().__init__()
        if  static.context is not None:
            self.mesh = VertColorMesh.get_cube_data(static.context,VColorShaderContainer())
        else :
            raise ValueError("まだinitされていないようです")
        self.set_bounding_obj(Vector3(-0.5,-0.5,-0.5),Vector3(0.5,0.5,0.5))
    @staticmethod
    def transform (
            position=Vector3(0,0,0),
            rotation=Vector3(0,0,1),
            scale=Vector3(1,1,1)
    )-> VColorCube :
        f = VColorCube()
        f.set_position(position)
        f.set_rotation(rotation)
        f.set_scale(scale)
        return f

class VColorFloor (Sprite3D) :
    mesh : MeshLike | None
    def __init__(self) -> None:
        super().__init__()
        import PyGame3d.static as static
        if static.context is not None:
            self.mesh = VertColorMesh.get_checkerboad_mesh(static.context,VColorShaderContainer(),color1=(0.0,0.5,0.0),color2=(0.01,0.01,0.01))
        else :
            raise ValueError("まだinitされていないようです")
        self.set_bounding_obj(Vector3(-20,-5,-20),Vector3(20,0,20))
    @staticmethod
    def transform (
            position=Vector3(0,0,0),
            rotation=Vector3(0,0,1),
            scale=Vector3(1,1,1)
    )-> VColorFloor :
        f = VColorFloor()
        f.set_position(position)
        f.set_rotation(rotation)
        f.set_scale(scale)
        return f
      
class Floor (Sprite3D) :
    mesh : MeshLike | None
    def __init__(self) -> None:
        super().__init__()
        import PyGame3d.static as static
        if static.context is not None:
            self.mesh = UVSubMesh.floor_mesh(color=(0.3,0.3,0.1))
        else :
            raise ValueError("Not yet excuse Application.init() . \n First line in your source code is \n```py\nimport PyGame3d as pg\ngame=pg.Application(fps=60)\ngame = pg.init()\n```")
        self.set_bounding_obj(Vector3(-20,-5,-20),Vector3(20,0,20))
    @staticmethod
    def transform (
            position=Vector3(0,0,0),
            rotation=Vector3(0,0,1),
            scale=Vector3(1,1,1)
    )-> Floor :
        f = Floor()
        f.set_position(position)
        f.set_rotation(rotation)
        f.set_scale(scale)
        return f  
class CuttingBoad (Sprite3D) :
    def __init__(self,tex_filepath:str) -> None:
        super().__init__()
        self.mesh = UVSubMesh.cutting_boad(tex_filepath)
        self.set_bounding_obj(Vector3(-0.5,-0.5,0),Vector3(0.5,0.5,0))
    @staticmethod
    def transform (
            tex_filepath:str,
            position=Vector3(0,0,0),
            rotation=Vector3(0,0,1),
            scale=Vector3(1,1,1)
    )-> CuttingBoad :
        f = CuttingBoad(tex_filepath)
        f.set_position(position)
        f.set_rotation(rotation)
        f.set_scale(scale)
        return f

class FPSPlayer (Sprite3D) :
    # pointer
    _look_at : Vector3
    perspect : Camera
    _mouse : Vector2
    _screen_center : tuple[int,int] | None
    xz_angle : float
    y_angle : float
    sensitibity : float
    is_mouse_rock : bool 
    _esc_was_down : bool
    from PyGame3d.GameObject.Camera import Camera
    def __init__(self,camera:Camera,sensitibity=1/200,is_mouse_rock=True) -> None:
        super().__init__(
            name="player"
        )
        mouse = pygame.mouse.get_pos()
        self._mouse = Vector2(*mouse)
        self._look_at = Vector3(0,0,1)
        self.perspect = camera
        self.position += Vector3(0,4,0)
        self.set_collide_enabled(True)
        self.set_velocity_enabled(True)
        self.xz_angle = 0
        self.y_angle = 0
        self.sensitibity = sensitibity
        self._screen_center = None
        self.is_mouse_rock = is_mouse_rock
        self._esc_was_down = False
        self._lock_mouse_to_center()
        self.set_bounding_obj(Vector3(-0.5,-1,-0.5),Vector3(0.5,0,0.5))
    def update(self, delta_time: float):
        mouse = Vector2(*pygame.mouse.get_pos())
        if self.is_mouse_rock:
            self._lock_mouse_to_center()
            delta = mouse - self._mouse
        else:
            self._unlock_mouse()
            delta = Vector2(0,0)

        
        self.xz_angle -= delta.x*self.sensitibity
        self.y_angle  -= delta.y*self.sensitibity
        if self.y_angle >= 1.570796 :
            self.y_angle = 1.579706
        elif self.y_angle <= -1.570796 :
            self.y_angle = -1.579706

        c = math.cos(self.y_angle)
        self._look_at.x = math.sin(self.xz_angle)*c
        self._look_at.z = math.cos(self.xz_angle)*c
        self._look_at.y = math.sin(self.y_angle)
        
        self.perspect.position = self.position
        self.perspect.look_at(self._look_at+self.position)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] :
            self.add_position(Vector3(self._look_at.x,0,self._look_at.z).normalized()*delta_time)
        if keys[pygame.K_s] :
            self.add_position(-Vector3(self._look_at.x,0,self._look_at.z).normalized()*delta_time)
        if keys[pygame.K_a] :
            self.add_position(Vector3(self._look_at.z,0,self._look_at.x).normalized()*delta_time)
        if keys[pygame.K_d] :
            self.add_position(-Vector3(self._look_at.z,0,self._look_at.x).normalized()*delta_time)
        esc_now = keys[pygame.K_ESCAPE]
        if esc_now and not self._esc_was_down:
            self.is_mouse_rock = not self.is_mouse_rock
            if self.is_mouse_rock:
                self._lock_mouse_to_center()
            else:
                self._unlock_mouse()
                # reset delta baseline when unlocked
                self._mouse = Vector2(*pygame.mouse.get_pos())
        self._esc_was_down = esc_now
        if keys[pygame.K_SPACE] :
            if abs(self.physics.velocity.y) <= 0.001 :
                print("jump")
                self.physics.velocity.y += 9.81
        if self.position.y <= - 50 :
            self.set_position(Vector3(0,4,0))
        return super().update(delta_time)

    def _lock_mouse_to_center(self) -> None:
        surface = pygame.display.get_surface()
        if surface is None:
            return
        if self._screen_center is None:
            self._screen_center = surface.get_rect().center
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        pygame.mouse.set_pos(self._screen_center)
        self._mouse = Vector2(*self._screen_center)

    def _unlock_mouse(self) -> None:
        pygame.event.set_grab(False)
        pygame.mouse.set_visible(True)
