import board
import pixelstrip
import math
import random
from colors import *


class ImageAnimation(pixelstrip.Animation):

    def __init__(self):
        pixelstrip.Animation.__init__(self)
        self.width = 8
        self.height = 8
        self.time = 0
        self.list = [1,2,3,4,5,6,7,8]
        self.shuffle()
        self.cursor = 0
        self.correct = True
        self.timeout2 = 0

    def shuffle(self):
        self.list = []
        for i in range(self.width):
            self.list.append(random.randrange(2,9))

    def reset(self, matrix):
        self.timeout = 0.1
        matrix.clear()
        matrix.show()

    def draw(self, matrix, delta_time):
        if self.is_timed_out():
            self.draw_image(matrix)
            matrix.show()
            self.timeout = 0.0
    
    def draw_image(self, matrix):
        if self.timeout2 > 0:
            self.timeout2 -= 1
            return
        if self.timeout2 == 0:
            self.shuffle()
            self.cursor = 0
            self.correct = True
            self.timeout2 = -1
            return
        if self.cursor == self.width-1:
            if self.correct:
                self.timeout2 = 100
                return
            else:
                self.cursor = 0
                self.correct = True
        if self.list[self.cursor] > self.list[self.cursor+1]:
            self.correct = False
            self.list[self.cursor], self.list[self.cursor+1] = self.list[self.cursor+1], self.list[self.cursor]
        self.cursor += 1
        currentTime = self.time
        matrix.fill(BLACK)
        for i in range(8):
            # print(self.imgdata[frame])
            for j in range(8):
                color = (255,255,255)
                if self.cursor > i and self.correct: 
                    color = (0,255,0)
                if self.cursor == i:
                    color = (255,0,0)
                if self.list[i] > j:
                    matrix[i, j] = color

if __name__ == "__main__": 
    matrix1 = pixelstrip.PixelStrip(board.GP15, width=8, height=8, bpp=4, pixel_order=pixelstrip.GRB, options={pixelstrip.MATRIX_COLUMN_MAJOR, pixelstrip.MATRIX_ZIGZAG})
    matrix1.animation = ImageAnimation()
    while True:
        matrix1.draw()
