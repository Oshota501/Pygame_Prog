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
    """
    ### 重要
    このlistは通常のlistと異なり、removeで最適化されている一方で**removeするときに物理配列のindexを指定**する必要があります。\n
    理論配列のindexを指定して削除したい場合はremove_source(index)を実行して下さい。ただし計算量は O(n) になります。
    ### 概要
    このlistはremoveとappendについて O(1) で実行可能ですが\n
    insert(index,value)とget(index) に計算量 O(n) を要します。\n
    release_get(index) は初回計算量 O(n) で操作を加えない場合以降 O(1) で可能です\n

    ### 注釈:\n
    初期設定では無効な値が50%を超えたときにメモリー解放を行うようになっています。\n
    - 解決策:\n
    引数に次の文を追加するとプロセス終了までメモリ内に値を保持した状態になります。\n
    ```
    release_option=FragList.ReleaseOption(
        release_ratio=0,
    )
    
    ```
    なおprivateメソットに触れると動作がバグるのでやめて下さい。
    """
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
    def __next__(self) -> _Type:
        while True:
            # 物理的なリスト長で終了判定することで、無効要素を含む場合も正しく終端します
            if self._current >= self._all_length:
                raise StopIteration
            entry = self._fraglist[self._current]
            self._current += 1
            if entry.is_valid:
                return entry.value
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
    def get_encode_list (self) -> list[_Type] :
        return [t.value for t in self._fraglist if t.is_valid]
    def release_get(self, index: int) -> _Type | None:
        # 有効要素としてのインデックス境界を先に確認
        if not (0 <= index < self.length):
            return None
        if self._all_length == self.length:
            # 無効要素が存在しない場合はそのまま O(1)
            return self._fraglist[index].value
        else:
            # 初回のみ release により O(n)、以降は O(1)
            self.release()
            return self._fraglist[index].value
    def append (self,value:_Type) -> None:
        self._all_length += 1
        self.length += 1
        self._fraglist.append(FragEntry(True,value))
        self.check_size_release()
        return 
    def remove (self,index:int) -> bool:
        """
        物理インデックス（有効要素の中での位置）で要素を削除します。
        計算量: O(1)
        """
        if 0 <= index < self._all_length and self._fraglist[index].is_valid:
            self.length -= 1
            self._fraglist[index].is_valid = False
            self.check_size_release()
            return True
        return False
        
    def remove_source (self,index:int) -> bool :
        """
        論理インデックス（有効要素の中での位置）で要素を削除します。
        計算量: O(n)
        """
        if not (0 <= index < self.length):
            return False
        
        # 有効要素を数えながら、削除位置を探す
        count = 0
        for i, entry in enumerate(self._fraglist):
            if entry.is_valid:
                if count == index:
                    # この位置を無効化
                    self._fraglist[i].is_valid = False
                    self.length -= 1
                    self.check_size_release()
                    return True
                count += 1
        return False
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
    def __str__ (self) -> str :
        result = "["
        for a in self :
            result += str(a) + ","
        result += "]"
        return result
    def insert(self, index: int, value: _Type) -> None:
        if not (0 <= index <= self.length):
            raise IndexError("index out of range")
        
        # 有効要素を数えながら、挿入位置を探す
        count = 0
        insert_pos = len(self._fraglist)  # デフォルトは末尾
        
        for i, entry in enumerate(self._fraglist):
            if entry.is_valid:
                if count == index:
                    insert_pos = i
                    break
                count += 1
        
        self._fraglist.insert(insert_pos, FragEntry(True, value))
        self.length += 1
        self._all_length += 1
        self.check_size_release()
    def __getitem__ (self,key:int) -> _Type|None :
        return self.get(key)
    def __setitem__ (self,key:int,value:_Type) -> None :
        self.insert(key,value)
        return
    def __delitem__ (self,key:int) -> None :
        self.remove(key) 