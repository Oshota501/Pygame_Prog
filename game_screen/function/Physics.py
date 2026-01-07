import pygame 

class Physics :
    position : tuple[float,float]
    speed : tuple[float,float]
    def __init__(self,position:tuple[float,float]) -> None:
        self.position = position
        self.speed = (0.0,0.0)
        return