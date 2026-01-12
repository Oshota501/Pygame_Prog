from abc import ABC , abstractmethod
from PyGame3d.vector.Vector3 import Vector3
from PyGame3d.Draw.mesh import MeshLike,Transform

# 描画など内部的な処理に使うUpdataとStart 
class SimpleGameObject (ABC) :
    @abstractmethod
    def update (self,delta_MS:float) -> None :
        return
    @abstractmethod
    def start (self) -> None :
        return

class PositionComponent (ABC) :
    # position
    @abstractmethod
    def get_position (self) -> Vector3 :
        pass
    @abstractmethod
    def set_position (self,absolute_position: Vector3) -> None :
        pass
    @abstractmethod
    def add_position (self,delta_position:Vector3) -> None :
        pass
    @abstractmethod
    def get_localposition (self) -> Vector3 :
        pass
    @abstractmethod
    def set_localposition (self ,local_position:Vector3) -> None :
        pass
class RotationComponent (ABC) :
    # rotation
    @abstractmethod
    def get_rotation (self) -> Vector3 :
        pass
    @abstractmethod
    def set_rotation (self,absolute_rotation: Vector3) -> None :
        pass
    @abstractmethod
    def add_rotation (self,delta_rotation:Vector3) -> None :
        pass
    @abstractmethod
    def get_localrotation (self) -> Vector3 :
        pass
    @abstractmethod
    def set_localrotation (self ,local_rotation:Vector3) -> None :
        pass
class ScaleComponent (ABC) :
    # Scale
    @abstractmethod
    def get_scale (self) -> Vector3 :
        pass
    @abstractmethod
    def set_scale (self,absolute_position: Vector3) -> None :
        pass
    @abstractmethod
    def add_scale (self,delta_position:Vector3) -> None :
        pass
    @abstractmethod
    def get_localscale (self) -> Vector3 :
        pass
    @abstractmethod
    def set_localscale (self ,local_position:Vector3) -> None :
        pass

class ContainerComponent (
            SimpleGameObject,
            PositionComponent,
            RotationComponent,
            ScaleComponent,
            ABC
    ) :
    @abstractmethod
    def add_child (self,object:ContainerComponent) -> None :
        pass
    @abstractmethod
    def remove_child(self,index:int) -> None :
        pass
    @abstractmethod
    def get_child (self) -> list[ContainerComponent] :
        pass
    @abstractmethod
    def get_parent (self) -> ContainerComponent | None :
        pass


class Sprite3DComponent (ContainerComponent,ABC) :
    @abstractmethod
    def get_mesh (self) -> MeshLike|None :
        pass



class GameContainer (ContainerComponent) :
    position : Vector3
    rotation : Vector3
    scale : Vector3
    child : list[ContainerComponent]
    parent : ContainerComponent | None
    def __init__(self) -> None:
        self.position = Vector3(0,0,0)
        self.scale = Vector3(1,1,1)
        self.rotation = Vector3(0,0,1)
        self.child = []
        self.parent = None
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
    def update (self,delta_MS:float) :
        for c in self.child :
            c.update(delta_MS)
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

class Sprite3D (
    GameContainer,
    Sprite3DComponent
) :
    mesh : MeshLike | None
    def __init__(self) -> None:
        super().__init__()
        self.mesh = None
    # @override
    def update(self,delta_MS:float):
        super().update(delta_MS)
        if self.mesh is not None :
            self.mesh.render(Transform(
                self.get_position(),
                self.get_rotation(),
                self.get_scale()
            ))
    def get_mesh(self) -> MeshLike|None:
        return self.mesh


