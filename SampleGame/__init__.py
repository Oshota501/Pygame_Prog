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
    CuttingBoad,
    StaticGameObject,
)
import pygame

from PyGame3d.GameObject.Collide import (
    CollisionDetectionContainer,
)
from PyGame3d.Singleton import SingletonABCMeta

AVAILABLE_FONT_PATH = "/System/Library/Fonts/ヒラギノ角ゴシック W1.ttc"

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
        font_path=AVAILABLE_FONT_PATH,
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
                "操作方法：WASDで移動、Spaceでジャンプ",
                (resolution[0] * 0.5, resolution[1] * 0.8),
            ),
            normal_font(
                "Start to Press Enter key", (resolution[0] * 0.5, resolution[1] * 0.5)
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
        if keys[pygame.K_RETURN]:
            set_game_scene(LoadingScene(Stage1))
        super().update(delta_time)


class Goal(StaticGameObject):
    player: FPSPlayer

    def __init__(self, player: FPSPlayer) -> None:
        self.player = player
        super().__init__(
            name="Goal",
            position=Vector3(61, 5, 61),
            rotation=Quaternion.look_rotation(Vector3(-61, 5, 61)),
            scale=Vector3(10, 10, 10),
            bounding_object=[
                StaticGameObject.get_bounging_Sphere(Vector3(61, 5, 61), 5)
            ],
            collide_enabled=True,
        )
        self.load_obj("./SampleGame/Assets/goal/goal.obj")

    def collide(self, other: CollisionDetectionContainer) -> None:
        self.player.set_position(Vector3(0, 0, 0))
        set_game_scene(LoadingScene(GameClear))
        return super().collide(other)


# シングルトン化することで何度もクソ重いインスタンス化をしなくて済むようになります。
# start関数でresetできるようにします。
class Stage1(Scene, metaclass=SingletonABCMeta):
    player: FPSPlayer
    gun: Sprite3D
    blocks: GameContainer
    explain: CuttingBoad

    def __init__(self) -> None:
        super().__init__()
        # player初期化時は物理演算を無効化
        self.player = FPSPlayer(self.get_camera())
        self.player.set_velocity_enabled(False)  # 物理演算OFF
        self.player.speed = 10
        self.player.jump_power = 0.7
        self.blocks = GameContainer("Blocks Container")
        self.explain = CuttingBoad.transform(
            "./SampleGame/Assets/explain.png",
            position=Vector3(12, 0, 0),
            scale=Vector3(30, 10, 1),
        )
        self.add_children(
            Floor.transform(Vector3(0, -5, 0)),
            self.player,
            self.blocks,
            CuttingBoad.transform(
                "./SampleGame/Assets/unity_3hours.png",
                position=Vector3(0, 0, -12),
                scale=Vector3(20, 10, 1),
                rotation=Quaternion.look_rotation(Vector3(0, 0, 12)),
            ),
            self.explain,
            Goal(self.player),
        )
        # playerの物理演算を有効化
        self.player.set_velocity_enabled(True)

    def start(self):
        super().start()
        self.player.set_position(Vector3(0, 0, 0))
        self.blocks.reset()

        for i in range(200):
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
        self.explain.look_at(self.player.get_position())


class GameOver(Scene):
    def __init__(self) -> None:
        resolution = game.screen_size
        super().__init__()
        self.add_children(
            UI_2d.color_rect((0.2, 0.2, 0.2, 1.0), Vector2(*resolution), resolution),
            normal_font("GameOver", (resolution[0] * 0.5, resolution[1] * 0.5)),
            normal_font(
                "Enter To Continue",
                (resolution[0] * 0.5, resolution[1] * 0.65),
                font_size=24,
            ),
        )

    def update(self, delta_time: float):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            set_game_scene(LoadingScene(Stage1))
        super().update(delta_time)


class GameClear(Scene):
    angle: float
    clear: UI_2d

    def __init__(self) -> None:
        resolution = game.screen_size
        self.angle = 0
        self.clear = normal_font(
            "GameClear",
            (resolution[0] * 0.5, resolution[1] * 0.4),
            font_color=(255, 255, 0),
            font_size=72,
        )
        super().__init__()
        self.add_children(
            UI_2d.color_rect((0.2, 0.2, 0.2, 1.0), Vector2(*resolution), resolution),
            self.clear,
            normal_font(
                "Enter To Continue",
                (resolution[0] * 0.5, resolution[1] * 0.65),
                font_size=24,
            ),
        )

    def update(self, delta_time: float):
        self.angle += delta_time
        resolution = game.screen_size
        self.clear.set_position(
            Vector3(
                resolution[0] * 0.5,
                resolution[1] * 0.3 - abs(math.sin(self.angle * 2.4) * 50),
                0,
            )
        )
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            set_game_scene(LoadingScene(Stage1))
        super().update(delta_time)
