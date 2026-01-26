import math
from PyGame3d.game import Application

class PerformanceInspectator :
    def __init__(self,app:Application) -> None:
        self.performance_sec = 0
        self.fps = 0
        self.fpss = []
        self.ffpss = []
        app.get_scene().ticker_add(self.update)
    @staticmethod
    def ave (ff) :
        sum = 0
        for f in ff :
            sum += f
        if len(ff) == 0 :
            return 0
        return sum / len(ff)
    def update (self,delta_time:float) -> None :
        self.performance_sec += delta_time
        self.fps += 1
        
        if self.performance_sec >= 1.0 :
            performance_sec = 0
            self.fpss.append(self.fps)
            self.ffpss.append(self.fps*self.fps)
            a = PerformanceInspectator.ave(self.fpss)
            print(f"n:{len(self.fpss)}, fps:{self.fps}, a:{math.floor(a)}, s:{math.floor((math.sqrt(PerformanceInspectator.ave(self.ffpss)-a*a))*100)*0.01}")
            fps = 0
