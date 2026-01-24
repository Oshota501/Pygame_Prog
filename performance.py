import math

performance_sec = 0
fps = 0
fpss = []
ffpss = []
def ave (ff) :
    sum = 0
    for f in ff :
        sum += f
    if len(ff) == 0 :
        return 0
    return sum / len(ff)
def update (delta_time:float) -> None :
    global performance_sec,fps,fpss,ffpss
    performance_sec += delta_time
    fps += 1
    
    if performance_sec >= 1.0 :
        performance_sec = 0
        fpss.append(fps)
        ffpss.append(fps*fps)
        a = ave(fpss)
        print(f"n:{len(fpss)}, fps:{fps}, a:{math.floor(a)}, s:{math.floor((math.sqrt(ave(ffpss)-a*a))*100)*0.01}")
        fps = 0