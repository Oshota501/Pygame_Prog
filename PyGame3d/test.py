# コードテスト用関数。
def start () :
    vec3test()
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

def vec3test () :
    from pg3_math.vector import Vector3

    v1 = Vector3(0,0,0)
    v2 = Vector3(0,0,0)
    assert v1 + v2 == Vector3(0,0,0)

    v1.x += 10
    v2.x += 10
    assert v1 == v2 
    print(v1,v2)
    