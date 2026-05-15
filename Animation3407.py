import pixelstrip
import random
import math

class Animation3407(pixelstrip.Animation):
    def __init__(self):
        self.image=(
            (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
            (0,0,1,1,1,0,0,0,0,2,0,0,0,2,0,0,0,0,3,3,3,3,0,0,0,4,4,4,4,4,4,0),
            (0,1,5,5,5,1,0,0,0,2,0,0,0,2,0,0,0,3,7,7,7,7,3,0,0,8,8,8,8,8,4,0),
            (0,5,0,1,1,5,0,0,0,2,0,0,0,2,0,0,0,3,0,0,0,0,3,0,0,0,0,0,0,4,8,0),
            (0,0,0,5,5,1,0,0,0,2,2,2,2,2,0,0,0,3,0,0,0,0,3,0,0,0,0,0,4,8,0,0),
            (0,1,0,0,0,1,0,0,0,6,6,6,6,2,0,0,0,3,0,0,0,0,3,0,0,0,0,4,8,0,0,0),
            (0,5,1,1,1,5,0,0,0,0,0,0,0,2,0,0,0,7,3,3,3,3,7,0,0,0,4,8,0,0,0,0),
            (0,0,5,5,5,0,0,0,0,0,0,0,0,6,0,0,0,0,7,7,7,7,0,0,0,0,8,0,0,0,0,0)   
        )
        self.colors = [[0,0,0],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[100,100,100],[100,100,100],[100,100,100],[100,100,100]]

        for i in range(8):
            self.colors.append([i*8,i*8,i*8])



        self.t=0
    def draw(self, strip, delta_time):
        self.t+= 0.01
        for i in range(4):
            color = [100+(math.sin(i+t)+1)*100,100+(math.sin(i+t*1.1)+1)*100,100+(math.sin(i+t*1.2)+1)*100]
            self.colors[i+1] = color
            self.colors[i+5] = [color[0]*0.5,color[1]*0.5,color[2]*0.5]
        for y in range(8):
            for x in range(32):
                if (self.image[y][x] == 0): continue
                strip[x,y]=self.colors[self.image[y][x]]
        strip.show()

if __name__ == "__main__":
    strip = pixelstrip.PixelStrip(width=32, height=8)
    strip.wrap = True
    strip.timeout = 0.0
    # while True:
