from .game import Application

# 数値型
from .vector import Vector3
from .vector import Vector2
from .vector import Quaternion
from .matrix.mat4 import Matrix4

# c++ を使う場合は "sh setup.sh" を実行
# from pg3_math.matrix import Matrix4
# from pg3_math.vector import Vector3
# パフォーマンス
from .performance import PerformanceInspectator

# シーン
from .Scene import Scene

# ゲームオブジェクト
from .GameObject.Camera import Camera

# from .GameObject.Collide import
from .GameObject.Container import GameContainer
from .GameObject.sprite import Sprite3D
from .GameObject.ui_2d import UI_2d

# サンプル
from .GameObject.Sample import CuttingBoad, Floor
from .GameObject.Sample.player import Player, FPSPlayer
from .GameObject.Sample.Cube import Cube, StaticCube, VColorCube

__all__ = [
    "Application",
    "Vector3",
    "Vector2",
    "Matrix4",
    "PerformanceInspectator",
    "Scene",
    "Camera",
    "GameContainer",
    "Sprite3D",
    "Cube",
    "StaticCube",
    "VColorCube",
    "CuttingBoad",
    "Floor",
    "UI_2d",
    "Quaternion",
    "Player",
    "FPSPlayer",
]
