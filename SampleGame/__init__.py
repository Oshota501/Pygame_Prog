import math
import random
from PyGame3d import (
    Application,
    Scene,
    UI_2d,
    Vector3,
    Vector2,
    Quaternion,
    Floor,
    FPSPlayer,
    Sprite3D,
    GameContainer,
    StaticCube,
    PerformanceInspectator,
)
import pygame

from PyGame3d.Singleton import SingletonABCMeta

game = Application()


def main() -> None:
    game.init()
    game.set_scene(StartScene())
    game.start_rendering()


def set_game_scene(scene: Scene) -> None:
    game.set_scene(scene)


def normal_font(
    text: str,
    position: tuple[float, float] | None = None,
    font_size=40,
    font_color=(255, 255, 255),
) -> UI_2d:
    result = UI_2d.text(
        text=text,
        resolution_pointer=game.screen_size,
        font_size=font_size,
        color=font_color,
        font_path="/System/Library/Fonts/ヒラギノ角ゴシック W1.ttc",
    )
    if position is None:
        result.place_screen_center()
    else:
        result.set_position(Vector3(position[0], position[1], 0))
    return result


class LoadingScene(Scene):
    def __init__(self, next_scene_class):
        super().__init__()
        self.next_scene_class = next_scene_class
        # テキスト作成
        self.loading_text = normal_font("Now Loading...")
        self.add_child(self.loading_text)

        # フレームカウンター
        self.frame_count = 0

    def update(self, delta_time: float):
        super().update(delta_time)

        self.frame_count += 1

        # 1フレーム目は「Now Loading」を描画させるためにスルーします。
        # 2フレーム目に入った瞬間（画面にはLoadingが出ている状態）に重い処理を走らせます。
        if self.frame_count == 2:
            # ここで2秒間フリーズしますが、
            # 画面は "Now Loading..." が表示された状態で止まるので違和感はありません。
            target_scene = self.next_scene_class()

            # 読み込み終わったらシーン遷移
            set_game_scene(target_scene)


class StartScene(Scene):
    time: float
    title_pos: tuple[float, float]
    title: UI_2d

    def __init__(self) -> None:
        super().__init__()
        self.time = 0
        resolution = game.screen_size
        self.title_pos = (resolution[0] * 0.5, resolution[1] * 0.2)
        self.title = normal_font("アスレチックゲーム", self.title_pos, 80)
        self.add_children(
            UI_2d.color_rect((0.2, 0.2, 0.2, 1.0), Vector2(*resolution), resolution),
            self.title,
            normal_font(
                "Start to Press Space key", (resolution[0] * 0.5, resolution[1] * 0.5)
            ),
            normal_font(
                "製作者: oshota",
                (resolution[0] * 0.5, resolution[1] * 0.65),
                font_size=24,
            ),
        )

    def update(self, delta_time: float):
        self.time += delta_time
        resolution = game.screen_size
        self.title_pos = (
            resolution[0] * 0.5,
            resolution[1] * 0.3 - abs(math.sin(self.time * 2.4) * 50),
        )
        self.title.set_position(Vector3(self.title_pos[0], self.title_pos[1], 0))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            set_game_scene(LoadingScene(Stage1))
        super().update(delta_time)


# シングルトン化することで何度もクソ重いインスタンス化をしなくて済むようになります。
# start関数でresetできるようにします。
class Stage1(Scene, metaclass=SingletonABCMeta):
    player: FPSPlayer
    gun: Sprite3D
    blocks: GameContainer

    def __init__(self) -> None:
        super().__init__()
        # player初期化時は物理演算を無効化
        PerformanceInspectator(self)
        self.player = FPSPlayer(self.get_camera())
        self.player.set_velocity_enabled(False)  # 物理演算OFF
        self.player.speed = 10
        self.player.jump_power = 0.7
        self.blocks = GameContainer("Blocks Container")
        self.add_children(Floor.transform(Vector3(0, -5, 0)), self.player, self.blocks)
        # playerの物理演算を有効化
        self.player.set_velocity_enabled(True)

    def start(self):
        super().start()
        self.player.set_position(Vector3(0, 0, 0))
        self.blocks.reset()
        for i in range(100):
            cube = StaticCube(
                position=Vector3(
                    random.random() * 80,
                    random.random() * 10 - 5,
                    random.random() * 80,
                ),
                rotation=Quaternion.identity(),
                scale=Vector3(1, 0.2, 1),
                color=(random.random(), random.random(), random.random(), 1),
            )
            self.blocks.add_child(cube)

    def update(self, delta_time: float):
        super().update(delta_time)
        if self.player.position.y <= -10:
            set_game_scene(LoadingScene(GameOver))


class GameOver(Scene):
    def __init__(self) -> None:
        resolution = game.screen_size
        super().__init__()
        self.add_children(
            UI_2d.color_rect((0.2, 0.2, 0.2, 1.0), Vector2(*resolution), resolution),
            normal_font("GameOver", (resolution[0] * 0.5, resolution[1] * 0.5)),
            normal_font(
                "Space To Continue",
                (resolution[0] * 0.5, resolution[1] * 0.65),
                font_size=24,
            ),
        )

    def update(self, delta_time: float):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            set_game_scene(LoadingScene(Stage1))
        super().update(delta_time)
