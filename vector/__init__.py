from abc import ABC , abstractmethod

class Vector3Like :
    @abstractmethod
    def get_tuple (self) -> tuple[float,float,float] :
        pass
