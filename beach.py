import pixelstrip
import board
import time
import math
import random

class BeachAnimation(pixelstrip.Animation):
    def __init__(self):
        pixelstrip.Animation.__init__(self)
        self.imgdata = [[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]]
        self.colorlist = [(0, 0, 0)]

        # matrix = pixelstrip.PixelStrip(board.GP15, width=len(self.imgdata[0][0]), height=len(self.imgdata[0]), bpp=4, pixel_order=pixelstrip.GRB, 
        #                         options={pixelstrip.MATRIX_COLUMN_MAJOR, pixelstrip.MATRIX_ZIGZAG}, brightness=0.3)

        # matrix.timeout = 0.0

        # matrix.clear()

        self.current_frame = 0
        self.currentTime = 0
        self.height = len(self.imgdata[0][0])
        self.balls = []
        for i in range(4):
            angle = random.uniform(0,math.pi*2)
            self.balls.append([[i*5,0],[math.cos(angle),math.sin(angle)]])
    def draw(self,matrix,dt):
        for i in range(len(self.imgdata[0][0])):
            #print(imgdata[current_frame])
            k = math.sin(i*0.3+self.currentTime*0.3)*0.4+4+math.sin(i*0.8+self.currentTime*0.3)*0.8
            for j in range(len(self.imgdata[0   ])):
                color = (0,100,255)
                if (j < k):
                    color = (0,0,255)
                if (abs(j-k)<0.6):
                    color = (255,255,255)
                matrix[self.height-1-i, j] = color
        for i in range(len(self.balls)):
            self.balls[i][1][1] += 0.2
            if (self.balls[i][0][1] > math.sin(self.balls[i][0][1]*0.3+self.currentTime*0.3)*0.4+4+math.sin(self.balls[i][0][1]*0.8+self.currentTime*0.3)*0.8):
                self.balls[i][1][1] -= 0.21
            self.balls[i][0][0] += self.balls[i][1][0]
            self.balls[i][0][1] += self.balls[i][1][1]

            if (self.balls[i][0][0] < 0):
                self.balls[i][1][0] = abs(self.balls[i][1][0])
                self.balls[i][0][0] = 0
            if (self.balls[i][0][0] > 32):
                self.balls[i][1][0] = -abs(self.balls[i][1][0])
                self.balls[i][0][0] = 32
            if (self.balls[i][0][1] < 0):
                self.balls[i][1][1] = abs(self.balls[i][1][0])
                self.balls[i][0][1] = 0
            if (self.balls[i][0][1] > 7):
                self.balls[i][1][1] = -abs(self.balls[i][1][0])
                self.balls[i][0][1] = 7

            matrix[math.floor(self.balls[i][0][0]), math.floor(self.balls[i][0][1])] = (255,0,0)
        matrix.show()
        time.sleep(0)
        self.current_frame += 1
        self.currentTime += 1
        if self.current_frame >= len(self.imgdata): self.current_frame = 0

# while True:

if __name__ == "__main__": 
    matrix1 = pixelstrip.PixelStrip(board.GP15, width=32, height=8, bpp=4, pixel_order=pixelstrip.GRB, options={pixelstrip.MATRIX_COLUMN_MAJOR, pixelstrip.MATRIX_ZIGZAG})
    matrix1.animation = BeachAnimation()
    while True:
        matrix1.draw()
