# coding by oshota 

import math
import pygame
from PyGame3d.Draw import MeshLike
from PyGame3d.Draw.texture import UVTexture
from PyGame3d.Draw.uvmesh import UV3dMeshSub
from PyGame3d.GameObject.sprite import Sprite3D, Sprite3DBoundingObject, Sprite3DPhysicsComponent
from PyGame3d.vector import Vector2, Vector3

class Player (Sprite3D) :
    # pointer
    _look_at : Vector3
    _mouse : Vector2
    _screen_center : tuple[int,int] | None
    xz_angle : float
    y_angle : float
    sensitibity : float
    is_mouse_rock : bool 
    _esc_was_down : bool
    
    def __init__(self,sensitibity=1/200,is_mouse_rock=True) -> None:
        super().__init__(
            name="player"
        )
        mouse = pygame.mouse.get_pos()
        self._mouse = Vector2(*mouse)
        self._look_at = Vector3(0,0,1)
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
        self.physics.coefficient = 0
    def update(self, delta_time: float):
        if self.is_mouse_rock:
            mouse = Vector2(*pygame.mouse.get_pos())
            delta = mouse - self._mouse
            # マウスを中央に戻し、次フレームの基準位置を更新
            self._lock_mouse_to_center()
        else:
            self._unlock_mouse()
            delta = Vector2(0,0)

        
        self.xz_angle -= delta.x*self.sensitibity
        self.y_angle  -= delta.y*self.sensitibity
        # 真上・真下を向けるように制限を少し緩める（完全な±π/2ではなく、少し手前まで）
        max_pitch = 3.14159265 * 0.49  # 88.2度程度
        if self.y_angle >= max_pitch :
            self.y_angle = max_pitch
        elif self.y_angle <= -max_pitch :
            self.y_angle = -max_pitch

        c = math.cos(self.y_angle)
        self._look_at.x = math.sin(self.xz_angle)*c
        self._look_at.z = math.cos(self.xz_angle)*c
        self._look_at.y = math.sin(self.y_angle)

        keys = pygame.key.get_pressed()
        # 前後方向ベクトル（Y成分は0にして水平移動のみ）
        forward = Vector3(self._look_at.x, 0, self._look_at.z).normalized()
        # 右方向ベクトル（前方向を90度右に回転）
        right = Vector3(self._look_at.z, 0, -self._look_at.x).normalized()
        
        if keys[pygame.K_w] :
            self.add_position(forward * delta_time)
        if keys[pygame.K_s] :
            self.add_position(-forward * delta_time)
        if keys[pygame.K_d] :
            self.add_position(-right * delta_time)
        if keys[pygame.K_a] :
            self.add_position(right * delta_time)
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
            self.is_collide = False
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

class FPSPlayer (Player) :
    from PyGame3d.GameObject.Camera import Camera
    perspect : Camera
    def __init__(self, camera : Camera ,sensitibity=1 / 200, is_mouse_rock=True) -> None:
        super().__init__(sensitibity, is_mouse_rock)
        self.perspect = camera
    def update(self, delta_time: float):
        super().update(delta_time)
        self.perspect.position = self.position
        self.perspect.look_at(self._look_at+self.position)
    