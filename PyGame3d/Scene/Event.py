from warnings import deprecated
from PyGame3d.vector.Vector2 import Vector2

# signature : oshota
@deprecated("PyGame3ds event depends pygame event. This class not yet Implementation .")
class EventListener :
    event_type : int
    event : function
    def __init__(self,event_type:int,event_listener:function) -> None:
        self.event_type = event_type
        self.event = event_listener
    def event_happen (self,pos:Vector2) -> None :
        self.event(pos)
