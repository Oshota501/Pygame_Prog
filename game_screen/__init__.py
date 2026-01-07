import pygame
from abc import ABC , abstractmethod

class ScreenObject (ABC) :
    @abstractmethod
    def blit (self,parent:pygame.Surface,deltatime:float) -> None :
        pass

class Screen (ABC):
    @abstractmethod
    def __init__(self, screen: pygame.Surface) -> None:
        pass
    
    @abstractmethod
    def blit(self, screen: pygame.Surface,deltatime: float) -> None|Screen:
        pass


class ScreenContainer(ScreenObject):
    rect : pygame.Rect
    children : list[ScreenObject]

    def __init__(self, rect:pygame.Rect):
        self.rect = rect
        self.children = []
    
    def addChild(self, child: ScreenObject):
        self.children.append(child)
    
    def blit(self, parent_surface: pygame.Surface,deltatime:float) -> None:
        # 親 Surface に自分の領域を描画
        # 子要素も描画
        for child in self.children:
            child.blit(parent_surface,deltatime)
