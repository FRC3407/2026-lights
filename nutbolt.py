import board
import pixelstrip
import math
from colors import *


class ImageAnimation(pixelstrip.Animation):

    def __init__(self, cycle_time=0.5):
        pixelstrip.Animation.__init__(self)
        self.cycle_time = cycle_time
        self.current_frame = 0
        self.imgdata = [[[0,0,0,0],[1,2,3,1],[4,4,4,5],[4,4,4,6],[4,4,4,4],[4,4,4,4],[4,5,4,4],[0,0,0,0]],[[7,8,3,3],[2,2,8,2],[4,4,4,5],[4,4,4,6],[4,4,4,4],[4,4,4,4],[4,5,4,4],[9,5,4,4]],[[8,2,8,8],[10,11,2,11],[2,2,2,10],[4,4,4,6],[4,4,4,4],[4,4,4,4],[4,5,4,4],[9,5,4,4]],[[12,12,12,12],[13,13,12,13],[12,12,12,14],[4,4,4,6],[4,4,4,4],[4,4,4,4],[4,5,4,4],[9,5,4,4]],[[2,2,8,8],[11,11,2,11],[2,2,2,10],[10,10,8,11],[4,4,4,4],[4,4,4,4],[4,5,4,4],[9,5,4,4]],[[15,15,15,16],[17,17,15,17],[15,15,15,18],[15,18,16,17],[15,15,15,15],[4,4,4,4],[4,5,4,4],[9,5,4,4]],[[19,19,20,21],[22,22,19,22],[19,19,19,19],[19,19,21,22],[20,19,19,19],[4,4,4,4],[4,5,4,4],[9,5,4,4]],[[23,23,23,23],[24,25,23,25],[23,23,23,23],[23,23,23,25],[23,23,23,23],[23,23,23,23],[4,5,4,4],[9,5,4,4]],[[0,0,0,0],[26,26,26,26],[26,26,26,26],[26,26,27,26],[28,26,26,26],[26,27,26,27],[4,5,4,4],[0,0,0,0]],[[0,0,0,0],[29,29,30,29],[30,30,30,29],[29,29,30,29],[30,30,29,30],[29,30,30,30],[30,29,29,30],[0,0,0,0]]]
        self.colorlist = [(0, 0, 0), (52, 143, 108), (53, 143, 108), (52, 141, 107), (0, 34, 37), (0, 34, 38), (0, 35, 38), (52, 143, 107), (53, 143, 107), (0, 33, 36), (54, 143, 108), (54, 144, 108), (56, 144, 110), (57, 145, 111), (56, 145, 110), (35, 126, 94), (35, 126, 93), (36, 128, 94), (35, 128, 94), (17, 110, 81), (17, 110, 80), (17, 108, 80), (18, 110, 81), (1, 91, 68), (1, 92, 68), (1, 92, 69), (0, 66, 55), (0, 65, 54), (0, 66, 54), (0, 36, 39), (0, 36, 38)]
        self.imgdata2 = [[[0,1,1,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[1,1,1,1,2,2,3,2,2,3,2,2,3,2,2,3,2,2,3,2,2,3,2,2,3,2,2,3,2,2,2,2],[1,3,3,1,3,0,0,3,0,0,3,0,0,3,0,0,3,0,0,3,0,0,3,0,0,3,0,0,3,0,0,2],[3,3,3,3,4,3,1,1,3,1,1,3,1,1,3,1,1,3,1,1,3,1,1,3,1,1,3,1,1,3,1,1],[3,3,3,3,4,3,4,3,3,4,3,3,4,3,3,4,3,3,4,3,3,4,3,3,4,3,3,4,3,3,4,4],[4,3,3,4,4,4,4,5,4,4,5,4,4,5,4,4,5,4,4,5,4,4,5,4,4,5,4,4,5,4,4,2],[5,4,4,5,2,5,2,2,5,2,2,5,2,2,5,2,2,5,2,2,5,2,2,5,2,2,5,2,2,5,2,2],[5,5,5,5,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]]]
        self.colorlist2 = [(255, 161, 73), (255, 137, 39), (0, 0, 0), (255, 87, 0), (58, 20, 0), (16, 5, 0)]
        self.frames = len(self.imgdata)
        self.width = len(self.imgdata[0][0])
        self.height = len(self.imgdata[0])
        self.time = 0
        self.screwOffset = 4
        self.screwSpeed = 0.1

    def reset(self, matrix):
        self.timeout = self.cycle_time
        matrix.clear()
        for i in range(32):
            for j in range(8):
                l = i
                if l > 27:
                    l -= 28
                matrix[i, j] = self.colorlist2[self.imgdata2[0][j][l]]
        matrix.show()
        self.current_frame = 0

    def draw(self, matrix, delta_time):
        if self.is_timed_out():
            self.draw_image(matrix, self.current_frame)
            self.current_frame = (math.floor(self.screwOffset*4)) % self.frames
            matrix.show()
            self.screwOffset+= self.screwSpeed*0.5
            self.screwOffset = max(min(self.screwOffset,24),4)
            self.screwSpeed += (14-self.screwOffset)*0.005
            self.timeout = 0.01
            self.time += 1
    
    def draw_image(self, matrix, frame):
        currentTime = self.time
        # matrix.fill(BLACK)
        for i in range(2):
            k = math.floor(self.screwOffset)+i-math.floor(self.screwSpeed/abs(self.screwSpeed))*3+1
            if 0<=k<32:
                l = k
                if k>27:
                    l -= 28
            for j in range(8):
                    matrix[k, j] = self.colorlist2[self.imgdata2[0][j][l]]
                    # matrix[k, j] = (255,255,255)
        for i in range(8):
            # print(self.imgdata[frame])
            for j in range(4):
                # print("X")
                # print(i)
                # print(len(self.imgdata[self.current_frame]))
                # print("Y")
                # print(j)
                matrix[j+math.floor(self.screwOffset), i] = self.colorlist[self.imgdata[self.current_frame][i][j]]

if __name__ == "__main__": 
    matrix = pixelstrip.PixelStrip(board.GP15, width=32, height=8, bpp=4, pixel_order=pixelstrip.GRB, options={pixelstrip.MATRIX_COLUMN_MAJOR, pixelstrip.MATRIX_ZIGZAG})
    matrix.animation = ImageAnimation(0)
    while True:
        matrix.draw()
