"""
PyGame3d.GameObject.Sample.player の Docstring

FPSプレイヤー型を当たり判定なども含めて実装しています。
"""
import math
import pygame
from pygame.key import ScancodeWrapper
from PyGame3d.GameObject.sprite import Sprite3D
from PyGame3d.vector import Quaternion, Vector2, Vector3
from PyGame3d.GameObject.Camera import Camera

# coding by oshota
# pylint で 5 点は悲しい
# Too many 祖先 は無理すぎる。Pythonにもinterfaceがあったらな〜〜〜とか思うわけです。


class Player(Sprite3D):
    # pointer
    _look_at: Vector3
    _mouse: Vector2
    _screen_center: tuple[int, int] | None
    xz_angle: float
    y_angle: float
    sensitibity: float
    is_mouse_rock: bool
    _esc_was_down: bool

    def __init__(self, sensitibity=1 / 200, is_mouse_rock=False) -> None:
        super().__init__(name="player")
        mouse = pygame.mouse.get_pos()
        self._mouse = Vector2(*mouse)
        self._look_at = Vector3(0, 0, 1)
        self.position += Vector3(0, 4, 0)
        self.set_collide_enabled(True)
        self.set_velocity_enabled(True)
        self.xz_angle = 0
        self.y_angle = 0
        self.sensitibity = sensitibity
        self._screen_center = None
        self.is_mouse_rock = is_mouse_rock
        self._esc_was_down = False
        self._lock_mouse_to_center()
        self.set_bounding_obj(Vector3(-0.5, -1, -0.5), Vector3(0.5, 0, 0.5))
        self.physics.coefficient = 0
        # 環境設定
        self.speed = 1
        self.jump_power = 1

    def update(self, delta_time: float):
        if self.is_mouse_rock:
            mouse = Vector2(*pygame.mouse.get_pos())
            delta = mouse - self._mouse
            # マウスを中央に戻し、次フレームの基準位置を更新
            self._lock_mouse_to_center()
        else:
            self._unlock_mouse()
            delta = Vector2(0, 0)

        self.xz_angle -= delta.x * self.sensitibity
        self.y_angle -= delta.y * self.sensitibity
        # 真上・真下を向けるように制限を少し緩める（完全な±π/2ではなく、少し手前まで）
        max_pitch = 3.14159265 * 0.49  # 88.2度程度
        if self.y_angle >= max_pitch:
            self.y_angle = max_pitch
        elif self.y_angle <= -max_pitch:
            self.y_angle = -max_pitch

        c = math.cos(self.y_angle)
        self._look_at.x = math.sin(self.xz_angle) * c
        self._look_at.z = math.cos(self.xz_angle) * c
        self._look_at.y = math.sin(self.y_angle)

        self._keypress(delta_time)
        return super().update(delta_time)

    def _keypress(self, delta_time: float) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.set_velocity(Vector3(0, 0, self.speed))
        if keys[pygame.K_s]:
            self.set_velocity(Vector3(0, 0, -self.speed))
        if keys[pygame.K_a]:
            self.set_velocity(Vector3(self.speed, 0, 0))
        if keys[pygame.K_d]:
            self.set_velocity(Vector3(self.speed, 0, 0))
        if keys[pygame.K_SPACE]:
            self.is_collide = False
            self.set_velocity(Vector3(0, self.jump_power, 0))

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


class FPSPlayer(Player):
    perspect: Camera

    _pitch: float
    _yaw: float

    def __init__(self, camera: Camera, sensitibity=1 / 200, is_mouse_rock=True) -> None:
        super().__init__(sensitibity, is_mouse_rock)
        self.perspect = camera
        self.add_child(camera)
        self._pitch = 0
        self._yaw = 0

    def update(self, delta_time: float):
        # 親クラスのマウス処理とlook_at計算を実行
        # ただしキー入力処理は実行しない
        if self.is_mouse_rock:
            mouse = Vector2(*pygame.mouse.get_pos())
            delta = mouse - self._mouse
            self._lock_mouse_to_center()
        else:
            self._unlock_mouse()
            delta = Vector2(0, 0)

        self._yaw -= delta.x * self.sensitibity
        self._pitch -= delta.y * self.sensitibity

        max_pitch = 3.14159265 * 0.49
        if self._pitch > max_pitch: self._pitch = max_pitch
        if self._pitch < -max_pitch: self._pitch = -max_pitch

        q_yaw = Quaternion.from_euler(0, self._yaw, 0)
        q_pitch = Quaternion.from_euler(self._pitch, 0, 0)

        self.rotation = q_yaw
        self.perspect.rotation = q_pitch
        self._keypress(delta_time)

        return Sprite3D.update(self, delta_time)

    # override
    def _keypress(self, delta_time: float) -> None:
        """FPS視点での移動（プレイヤーの向きに依存）"""
        keys = pygame.key.get_pressed()
        sin_y = math.sin(self._yaw)
        cos_y = math.cos(self._yaw)
        # エンジンが「-Z」を前方とする場合:
        forward = Vector3(-sin_y, 0, -cos_y).normalized()
        right = Vector3(cos_y, 0, -sin_y).normalized() # Forwardの右90度

        self._mv_keypress(keys,forward,right,delta_time)

        self._esc_keypress(keys)
        self._jump_keypress(keys)

    def _mv_keypress(self,
                    keys: ScancodeWrapper,
                    forward: Vector3,
                    right: Vector3,
                    delta_time:float) -> None:
        if keys[pygame.K_w] :
            self.add_position(forward*delta_time)
        if keys[pygame.K_s] :
            self.add_position(-forward*delta_time)
        if keys[pygame.K_d] :
            self.add_position(right*delta_time)
        if keys[pygame.K_a] :
            self.add_position(-right*delta_time)

    def _mv_keypress_v(self,
                    keys:pygame.key.ScancodeWrapper,
                    forward:Vector3,
                    right:Vector3,
                    delta_time:float) -> None :
        move = Vector3(0, 0, 0)
        if keys[pygame.K_w]:
            move += forward
        if keys[pygame.K_s]:
            move -= forward
        if keys[pygame.K_d]:
            move += right
        if keys[pygame.K_a]:
            move -= right

        if move.length() > 0:
            move = move.normalized() * self.speed

        current_y = self.physics.velocity.y
        self.physics.velocity = Vector3(move.x, current_y, move.z)

    def _jump_keypress (self,keys:pygame.key.ScancodeWrapper) -> None :
        if keys[pygame.K_SPACE]:
            self.is_collide = False
            if abs(self.physics.velocity.y) <= 0.001:
                self.physics.velocity.y += 9.81 * self.jump_power

    def _esc_keypress (self,keys:pygame.key.ScancodeWrapper) -> None :
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
