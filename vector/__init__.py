from abc import ABC , abstractmethod

class Vector3Like(ABC) :
    @abstractmethod
    def get_tuple (self) -> tuple[float,float,float] :
        pass
