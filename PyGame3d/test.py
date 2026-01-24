# コードテスト用関数。
def start () :
    mat4text()
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
    import math

    v1 = Vector3(0,0,0)
    v2 = Vector3(0,0,0)
    assert v1 + v2 == Vector3(0,0,0)

    v1.x += 10
    v2.x += 10
    assert v1 == v2 

    v2.y = 10 
    v3 = v2.normalized()
    assert abs(math.sqrt(v3.x*v3.x + v3.y*v3.y + v3.z*v3.z)-1) <= 0.001
    d = v2.dot(v1)
    assert abs(d-100) <= 0.001

    print(v1,v2)

def mat4text () :
    from pg3_math.matrix import Matrix4

    m = Matrix4()
    m[2] = [0,10,10,0]
    m2 = Matrix4()

    print(m*m2)
