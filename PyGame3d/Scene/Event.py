from PyGame3d.vector.Vector2 import Vector2
from abc import ABC,abstractmethod

# signature : oshota
class EventListener :
    event_type : int
    event : function
    def __init__(self,event_type:int,event_listener:function) -> None:
        self.event_type = event_type
        self.event = event_listener
    def event_happen (self,pos:Vector2) -> None :
        self.event(pos)
