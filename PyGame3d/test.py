# コードテスト用関数。
def start () :
    return
def update () :
    return
    
def performance_test () :
    import time 
    import vector.FragList as vec

    a : vec.FragList[int] = vec.FragList([])
    t = time.time()
    for i in range(10000) :
        a.append(i)
    for i in range(10000) :
        a.remove((10000-i-1))
    print(str(a),time.time()-t)

    b : list[int] = []
    t = time.time()
    for i in range(10000) :
        b.append(i)
    for i in range(10000) :
        b.remove((10000-i-1))
    print(str(b),time.time()-t)