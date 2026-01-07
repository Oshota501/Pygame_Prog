from game_screen import ScreenObject
import pygame

class TextRender (
    ScreenObject
): 
    _textdata : str
    _fontsize : int
    _fontname : str
    _position : tuple[int,int]
    _fontweight : int
    _color : tuple[int,int,int]
    _textsurface : pygame.Surface
    _textrect : pygame.Rect
    _parent_rect : pygame.Rect

    def __init__(
            self,
            textdata : str ,
            parent_rect : pygame.Rect ,
            fontsize : int = 100 ,
            fontname : str = "ヒラキノ角コシックw0" ,
            position : tuple[int,int] = (0,0) ,
            fontweight : int = 60 ,
            color = (255,255,255)
    ) -> None:
        self._parent_rect = parent_rect
        self.reset_text(textdata,parent_rect,fontsize,fontname,position,fontweight,color)
        return 
    def reset_text (
            self,
            textdata : str ,
            parent_rect : pygame.Rect ,
            fontsize : int = 20 ,
            fontname : str = "ヒラキノ角コシックw0" ,
            position : tuple[int,int] = (0,0) ,
            fontweight : int = 10 ,
            color = (255,255,255)
    ) -> None:
        self._textdata = textdata
        self._fontname = fontname
        self._fontsize = fontsize
        self._position = position
        self._fontweight = fontweight
        self._color = color
        self._set_surface(parent_rect)
        return

    def _set_surface (self,parent_rect:pygame.Rect):
        is_bold = self._fontweight >= 700
        font = pygame.font.SysFont(
                self._fontname,
                self._fontsize,
                bold = is_bold
        )
        self._textsurface = font.render(self._textdata, True, self._color)
        c = parent_rect.center
        c2 = (c[0] + self._position[0] , c[1] + self._position[1] )
        self._textrect = self._textsurface.get_rect(center = c2)
    def set_text (self,text:str) -> None:
        self._textdata = text
        self._set_surface(self._parent_rect)
    def set_position (self,position:tuple[int,int]) -> None:
        self._position = position
        self._set_surface(self._parent_rect)
    def get_position (self) -> tuple[int,int] :
        return self._position 
    def blit (self,parent:pygame.Surface,deltatime:float) -> None :
        parent.blit(self._textsurface, self._textrect)
