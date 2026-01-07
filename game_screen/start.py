import pygame
from game_screen import Screen, ScreenContainer
from game_screen.function.TextRender import TextRender
import math

class StartScreen (Screen):
    _container : ScreenContainer
    _text_position : tuple[float,float] 
    _phase : float
    _text : TextRender
    def __init__(self,screen:pygame.Surface) :
        self._phase = 0.0
        self._text_position = (0,0)
        self._container = ScreenContainer(screen.get_rect())
        self._text = TextRender("Start",screen.get_rect())
        self._container.addChild(TextRender("クソゲー",screen.get_rect(),position=(0,-100)))
        self._container.addChild(self._text)
        return
    def blit(self,screen:pygame.Surface,deltatime: float) -> None | Screen:
        self._container.blit(screen,deltatime)
        self._text.set_position((int(self._text_position[0]),int(self._text_position[1])) )
        self._phase += 0.1
        self._text_position = (
            self._text_position[0]+math.sin(self._phase)*10+math.cos(self._phase)*10,
            self._text_position[1]+math.cos(self._phase)*10
       )
        return