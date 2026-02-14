import board
import pixelstrip
import math
import random
from colors import *


class ImageAnimation(pixelstrip.Animation):

    def __init__(self, cycle_time=0.5,offset=0):
        pixelstrip.Animation.__init__(self)
        self.cycle_time = cycle_time
        self.current_frame = 0
        self.imgdata = [[[0,0,1,1,1,1,0,0],[0,1,1,1,1,1,1,0],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[0,1,1,1,1,1,1,0],[0,0,1,1,1,1,0,0]]]
        self.colorlist = [(0, 0, 0), (255, 255, 255)]
        self.eyePosition = [4,4]
        self.eyeVelocity = [0,0]
        # self.eyePosition2 = [4,4]
        # self.eyeVelocity2 = [0,0]
        self.eyelid = 0

        self.frames = len(self.imgdata)
        self.width = len(self.imgdata[0][0])
        self.height = len(self.imgdata[0])
        self.time = offset

    def reset(self, matrix):
        self.timeout = self.cycle_time
        matrix.clear()
        matrix.show()
        self.current_frame = 0

    def draw(self, matrix, delta_time):
        if self.is_timed_out():
            self.draw_image(matrix, self.current_frame)
            self.current_frame = (self.current_frame + 1) % self.frames
            matrix.show()
            self.timeout = 0
            self.time += 1
    
    def draw_image(self, matrix, frame):
        currentTime = self.time
        matrix.fill(BLACK)
        for i in range(self.width):
            # print(self.imgdata[frame])
            for j in range(self.height):
                matrix[self.height-1-i, j] = self.colorlist[self.imgdata[self.current_frame][i][j]]
        matrix[math.floor(self.eyePosition[0]),math.floor(self.eyePosition[1])] = (0,0,0)
        matrix[math.floor(self.eyePosition[0]-1),math.floor(self.eyePosition[1])] = (0,0,0)
        matrix[math.floor(self.eyePosition[0]+1),math.floor(self.eyePosition[1])] = (0,0,0)
        matrix[math.floor(self.eyePosition[0]),math.floor(self.eyePosition[1])-1] = (0,0,0)
        matrix[math.floor(self.eyePosition[0]),math.floor(self.eyePosition[1])+1] = (0,0,0)
        self.eyeVelocity[0] += random.randrange(-10,10)*0.05
        self.eyeVelocity[1] += random.randrange(-10,10)*0.05
        self.eyeVelocity[0] *= 0.9
        self.eyeVelocity[1] *= 0.9
        self.eyePosition[0] += self.eyeVelocity[0]
        self.eyePosition[1] += self.eyeVelocity[1]
        self.eyeVelocity[1] += 0.35
        self.eyelid = math.pow(math.sin(self.time*0.05),500)-0.1
        if (math.sqrt(math.pow(self.eyePosition[0]-4,2)+math.pow(self.eyePosition[1]-4,2)) > 3.1):
            angle = math.atan2(self.eyePosition[1]-4,self.eyePosition[0]-4)
            n=[math.cos(angle),math.sin(angle)]
            dot = self.eyeVelocity[0]*n[0]+self.eyeVelocity[1]*n[1]
            self.eyeVelocity=[self.eyeVelocity[0]-2*dot*n[0],self.eyeVelocity[1]-2*dot*n[1]]
            self.eyePosition[0] = math.cos(angle)*3.1+4
            self.eyePosition[1] = math.sin(angle)*3.1+4
            # self.eyeVelocity[0] *= 1.2
            # self.eyeVelocity[1] *= 1.2
        for i in range(self.eyelid*4):
            for j in range(8):
                matrix[j,i] = (0,0,0)
                matrix[j,8-i] = (0,0,0)

if __name__ == "__main__": 
    matrix1 = pixelstrip.PixelStrip(board.GP15, width=8, height=8, bpp=4, pixel_order=pixelstrip.GRB, options={pixelstrip.MATRIX_COLUMN_MAJOR, pixelstrip.MATRIX_ZIGZAG})
    matrix1.animation = ImageAnimation(0,0)
    matrix2 = pixelstrip.PixelStrip(board.GP16, width=8, height=8, bpp=4, pixel_order=pixelstrip.GRB, options={pixelstrip.MATRIX_COLUMN_MAJOR, pixelstrip.MATRIX_ZIGZAG})
    matrix2.animation = ImageAnimation(0,2)
    while True:
        matrix1.draw()
        matrix2.draw()