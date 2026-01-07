import pygame
from pygame.locals import QUIT
import sys

SCREEN_RESOLUTION = (800,600)

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_RESOLUTION)
    clock = pygame.time.Clock()
    pygame.display.set_caption("クソゲー")
    
    # GameManagerをここでインポート（pygame初期化後）
    from GameManager import GameManager
    gm = GameManager(screen) 

    clock.tick(60)
    while (True):
        screen.fill((0,0,0))
        
        deltatime = clock.tick(60)
        gm.blit(deltatime)

        pygame.display.update()
        # イベント処理
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    main()
