import pixelstrip

from sort import *

class SortAnimation(pixelstrip.Animation):
    def __init__(self, sorttype: type[Sort], w, h, fps):
        pixelstrip.Animation.__init__(self)
        
        self.sorter = sorttype(w, h)
        self.FPS: int = fps
        
        self.frame: int = 0
    
    def draw(self, matrix, _delta_time):
        self.frame += 1
        
        if self.is_timed_out():
            self.timeout = 1.0 / self.FPS
            
            self.sorter.step()
            self.sorter.draw(matrix)
            
            matrix.show()
    
    def reset(self, matrix):
        self.timeout = 1.0 / self.FPS