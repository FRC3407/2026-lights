import board
import pixelstrip
import math
import random
import array
# from colors import *


class ImageAnimation(pixelstrip.Animation):

    def __init__(self, cycle_time=0.5):
        pixelstrip.Animation.__init__(self)
        self.cycle_time = cycle_time
        self.tickerBool = False

    def reset(self, matrix):
        self.timeout = self.cycle_time
        self.grid = []
        self.colorList = ((0,0,0),(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255),(255,100,0))
        self.tetrominos = (
            (2,2,1,1,1,1),
            (4,1,1,1,1,1),
            (3,2,1,1,1,1,0,0),
            (3,2,1,0,0,1,1,1),
            (3,2,1,1,0,0,1,1),
            (3,2,0,1,1,1,1,0),
            (3,2,0,1,0,1,1,1)
        )
        self.tetrominoPosition = [3,3]
        self.currentTetromino = 2
        self.rotation = 1
        for i in range(8):
            h = []
            for d in range(31):
                h.append(0)
            h.append(1)
            self.grid.append(h)
        # matrix.fill(BLACK)

    def draw(self, matrix, delta_time):
        if self.is_timed_out():
            self.draw_image(matrix)
            matrix.show()
    def draw_image(self,matrix):
        lowestPosition = (0,0)
        for i in range(8):
            for d in range(32):
                if d > lowestPosition[1]:
                    lowestPosition = (i,d)
                if self.grid[i][d] > 0:
                    break

        wantMove = random.randrange(-1,2)
        self.rotation += random.randrange(-1,2)
        if self.rotation > 3:
            self.rotation = 0
        for i in range(8):
            for d in range(32):
                g = self.grid[i][d]
                # print(g+1)
                matrix[d,i] = self.colorList[g] 
        preCurrentTetromino = self.tetrominos[self.currentTetromino]
        currentTetromino = []
        if self.rotation % 2 == 1:
            currentTetromino.append(preCurrentTetromino[1])
            currentTetromino.append(preCurrentTetromino[0])
            for i in range(preCurrentTetromino[0]):
                # print("i")
                # print((preCurrentTetromino[1]-1)*preCurrentTetromino[0]+i)
                for d in range((preCurrentTetromino[1]-1)*preCurrentTetromino[0]+i,i-1,-preCurrentTetromino[0]):
                    # print("d")
                    currentTetromino.append(preCurrentTetromino[d+2])
            # print(len(currentTetromino))
        else:
            for i in range(len(preCurrentTetromino)):
                currentTetromino.append(preCurrentTetromino[i])
        if self.rotation > 1:
            w = currentTetromino[0]
            h = currentTetromino[1]
            currentTetromino = currentTetromino[::-1]
            currentTetromino.insert(0,h)
            currentTetromino.insert(0,w)
        for i in range(currentTetromino[0]):
            for d in range(currentTetromino[1]):
                if currentTetromino[i+d*currentTetromino[0]+2] > 0:
                    if self.grid[max(min(i+self.tetrominoPosition[0],7),0)][d+self.tetrominoPosition[1]] > 0:
                        self.tetrominoPosition[1] -= 1
        hitGround = False
        for i in range(currentTetromino[0]):
            for d in range(currentTetromino[1]):
                if currentTetromino[i+d*currentTetromino[0]+2] > 0:
                    if self.grid[max(min(i+self.tetrominoPosition[0]+wantMove,7),0)][d+self.tetrominoPosition[1]+1] > 0:
                        wantMove = 0
        self.tetrominoPosition[0] += wantMove
        g=True
        while g:
            g = False
            for i in range(currentTetromino[0]):
                for d in range(currentTetromino[1]):
                    if (i+self.tetrominoPosition[0] < 0):
                        self.tetrominoPosition[0] +=1
                        # print("A")
                        g = True
                    if (i+self.tetrominoPosition[0] > 7):
                        # print("B")
                        self.tetrominoPosition[0] -=1
                        g = True
        for i in range(currentTetromino[0]):
            for d in range(currentTetromino[1]):
                # print(i
                # print(d)
                if currentTetromino[i+d*currentTetromino[0]+2] > 0:
                    if self.grid[i+self.tetrominoPosition[0]][d+self.tetrominoPosition[1]+1] > 0:
                        hitGround = True
                    # print(self.crrentTetromino+1)
                    # matrix[d+self.tetrominoPosition[1],i+self.tetrominoPosition[0]] = self.colorList[self.currentTetromino+1]
        self.tetrominoPosition[1] += 1
        if not hitGround:
            for i in range(currentTetromino[0]):
                for d in range(currentTetromino[1]):
                    # print(i
                    # print(d)
                    if currentTetromino[i+d*currentTetromino[0]+2] > 0:
                        if self.grid[i+self.tetrominoPosition[0]][d+self.tetrominoPosition[1]+1] > 0:
                            hitGround = True
                        # print(self.crrentTetromino+1)
                        matrix[d+self.tetrominoPosition[1],i+self.tetrominoPosition[0]] = self.colorList[self.currentTetromino+1]
        if hitGround:
            # self.tetrominoPosition[1] -= 1
            for i in range(currentTetromino[0]):
                for d in range(currentTetromino[1]):
                    if currentTetromino[i+d*currentTetromino[0]+2] > 0:
                        self.grid[i+self.tetrominoPosition[0]][d+self.tetrominoPosition[1]] = self.currentTetromino+1
            self.tetrominoPosition = [1,1]
            self.currentTetromino = random.randrange(0,6)
            self.rotation += 1
        # print("weenie")
if __name__ == "__main__": 
    matrix = pixelstrip.PixelStrip(width=32, height=8)
    matrix.animation = ImageAnimation(0)
    while True:
        matrix.draw()
