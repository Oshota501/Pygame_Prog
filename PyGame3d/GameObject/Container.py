import math
from PyGame3d.GameObject import ContainerComponent
from PyGame3d.vector import Vector3


class GameContainer (ContainerComponent) :
    position : Vector3
    rotation : Vector3
    scale : Vector3
    child : list[ContainerComponent]
    parent : ContainerComponent | None
    name : str
    def __init__(self,name="GameContainerName") -> None:
        self.position = Vector3(0,0,0)
        self.scale = Vector3(1,1,1)
        self.rotation = Vector3(0,0,1)
        self.child = []
        self.parent = None
        self.name = name
    def get_name (self) -> str :
        return self.name
    def add_child (self,object:ContainerComponent) -> None :
        pr_pointer = object.get_parent()
        if pr_pointer == None :
            pr_pointer = self 
            self.child.append(object)
            return
        else :
            print(f"Already registered with other container :{pr_pointer}")
            print("Registered faild.")
            return
    def add_children(self,children:list[ContainerComponent]) -> None :
        for child in children :
            self.add_child(child)
    def get_child(self) -> list[ContainerComponent]:
        return self.child
    def remove_child(self, index: int) -> None:
        pr_pointer = self.child[index].get_parent()
        pr_pointer = None
        del self.child[index]
    def get_parent(self) -> ContainerComponent | None:
        return self.parent 
    def start (self) :
        for c in self.child :
            c.start()
        return
    def update (self,delta_time:float) :
        for c in self.child :
            c.update(delta_time)
        return
    
    # Position
    def add_position(self, delta_position: Vector3) -> None:
        self.position += delta_position
    def get_position(self) -> Vector3:
        return self.position
    def set_position(self, absolute_position: Vector3) -> None:
        self.position = absolute_position
        return
    def get_localposition(self) -> Vector3:
        if self.parent == None :
            return self.position
        else :
            return self.position - self.parent.get_localposition() 
    def set_localposition(self, local_position: Vector3) -> None:
        if self.parent == None :
            self.set_position(local_position) 
        else :
            self.set_position(self.parent.get_position() + local_position)
        return
    
    # Rotation
    def add_rotation(self, delta_rotation: Vector3) -> None:
        self.rotation += delta_rotation
    def get_rotation(self) -> Vector3:
        return self.rotation
    def set_rotation(self, absolute_rotation: Vector3) -> None:
        self.rotation = absolute_rotation
        return
    def get_localrotation(self) -> Vector3:
        if self.parent == None :
            return self.rotation
        else :
            return self.rotation - self.parent.get_localrotation() 
    def set_localrotation(self, local_rotation: Vector3) -> None:
        if self.parent == None :
            self.set_rotation(local_rotation) 
        else :
            self.set_rotation(self.parent.get_rotation() + local_rotation)
        return
    def look_at(self, target_position: Vector3) -> None:
        dx,dy,dz = target_position - self.position
        distance_xz = math.sqrt(dx**2 + dz**2)
        # 注意: 座標系によっては dy の符号を変える必要があります
        pitch = -math.degrees(math.atan2(dy, distance_xz))
        yaw = math.degrees(math.atan2(dx, -dz))
        self.set_rotation(Vector3(pitch, yaw, 0.0))

    # Scale
    def add_scale(self, delta_scale: Vector3) -> None:
        self.scale += delta_scale
    def get_scale(self) -> Vector3:
        return self.scale
    def set_scale(self, absolute_scale: Vector3|int|float) -> None:
        if isinstance(absolute_scale,Vector3) :
            self.scale = absolute_scale
        else :
            self.scale *= absolute_scale
        return
    def get_localscale(self) -> Vector3:
        if self.parent == None :
            return self.scale
        else :
            return self.scale - self.parent.get_localscale() 
    def set_localscale(self, local_scale: Vector3) -> None:
        if self.parent == None :
            self.set_scale(local_scale) 
        else :
            self.set_scale(self.parent.get_scale() + local_scale)
        return
    @staticmethod
    def include_transform (
            position=Vector3(0,0,0),
            rotation=Vector3(0,0,1),
            scale=Vector3(1,1,1)
    ) -> GameContainer :
        g = GameContainer()
        g.set_position(position)
        g.set_rotation(rotation)
        g.set_scale(scale)
        return g