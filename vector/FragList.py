from typing import TypeVar, Generic, Optional, Iterable
from dataclasses import dataclass

_Type = TypeVar('_Type')

@dataclass
class ReleaseOption:
    release_ratio: float = 0.5
    release_min: int = 6


@dataclass
class FragEntry(Generic[_Type]):
    is_valid: bool
    value: _Type

class FragList (Generic[_Type]):
    _fraglist : list[FragEntry[_Type]]
    _current : int
    _all_length : int
    length : int
    release_opt : ReleaseOption
    def __init__(self, contentlist: Optional[Iterable[_Type]] = None, release_option: Optional[ReleaseOption] = None) -> None:
        items = list(contentlist) if contentlist is not None else []
        self._fraglist = [FragEntry(True, t) for t in items]
        self.length = len(items)
        self._all_length = len(items)
        self._current = 0
        self.release_opt = release_option if release_option is not None else ReleaseOption()
    def __iter__(self) -> FragList:
        self._current = 0
        return self 
    def __next__(self) -> _Type :
        while True :
            if self._current >= self.length:
                raise StopIteration
            entry = self._fraglist[self._current]
            self._current += 1
            if entry.is_valid:
                result = entry.value
                return result
    def __len__ (self) -> int :
        return self.length
    # 計算量nであることに注意して下さい。
    def get (self,index:int) -> _Type|None :
        if 0 <= index < self.length:
            count = 0
            for entry in self._fraglist:
                if entry.is_valid:
                    if count == index:
                        return entry.value
                    count += 1
        return None
    def append (self,value:_Type) -> None:
        self._all_length += 1
        self.length += 1
        self._fraglist.append(FragEntry(True,value))
        self.check_size_release()
        return 
    def remove (self,index:int) -> None:
        if 0 <= index < len(self._fraglist) and self._fraglist[index].is_valid:
            self.length -= 1
            self._fraglist[index].is_valid = False
        self.check_size_release()
        return 
    def check_size_release (self) :
        if self.length <= self.release_opt.release_min :
            return
        if self.length < self._all_length*self.release_opt.release_ratio :
            self.release()
    def release (self) -> None :
        new_list = [t for t in self._fraglist if t.is_valid]
        self._fraglist = new_list
        self.length = len(new_list)
        self._all_length = len(new_list)
        return