import vector

class Color (vector.Vector3Like):
    r : float
    g : float
    b : float
    def __init__(self,r:float,g:float,b:float) -> None:
        self.r = r
        self.g = g
        self.b = b
    def get_tuple (self) :
        return (self.r,self.g,self.b)

WHITE = Color(1.0,1.0,1.0)
RED = Color(1.0,0.0,0.0)
GREEN = Color(0.0,1.0,0.0)
BLUE = Color(0.0,0.0,1.0)
BLACK = Color(0.0,0.0,0.0)
