import vector 

class Vector3 (vector.Vector3Like):
    x : float 
    y : float 
    z : float
    def __init__(self,x:float=0.0,y:float=0.0,z:float=0.0) -> None:
        self.x = x
        self.y = y
        self.z = z
    
    def get_tuple(self) -> tuple[float, float, float]:
        return (self.x,self.y,self.z)