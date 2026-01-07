import pygame 
from game_screen.start import StartScreen
from game_screen import Screen


class GameManager :
    screen : Screen
    surface : pygame.Surface

    def __init__(self,screen : pygame.Surface) -> None:
        self.screen = StartScreen(screen)
        self.surface = screen

    def blit(self,deltatime:float) :
        next_screen = self.screen.blit(self.surface,deltatime)
        if next_screen == None :
            return
        else :
            self.screen = next_screen
            return
