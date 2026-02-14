import pixelstrip
import board
import time
import math
import random

imgdata = [[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]]
colorlist = [(0, 0, 0)]

matrix = pixelstrip.PixelStrip(board.GP15, width=len(imgdata[0][0]), height=len(imgdata[0]), bpp=4, pixel_order=pixelstrip.GRB, 
                        options={pixelstrip.MATRIX_COLUMN_MAJOR, pixelstrip.MATRIX_ZIGZAG}, brightness=0.3)

matrix.timeout = 0.0

matrix.clear()

current_frame = 0
currentTime = 0
height = len(imgdata[0][0])
balls = []
for i in range(4):
    balls.append([[i*5,0],[random.randrange(-1,1),random.randrange(-1,1)]])

while True:
    for i in range(len(imgdata[current_frame][0])):
        #print(imgdata[current_frame])
        k = math.sin(i*0.3+currentTime*0.3)*0.4+4+math.sin(i*0.8+currentTime*0.3)*0.8
        for j in range(len(imgdata[current_frame])):
            color = (0,100,255)
            if (j < k):
                color = (0,0,255)
            if (abs(j-k)<0.6):
                color = (255,255,255)
            matrix[height-1-i, j] = color
    for i in range(len(balls)):
        balls[i][1][1] += 0.2
        if (balls[i][0][1] > math.sin(balls[i][0][1]*0.3+currentTime*0.3)*0.4+4+math.sin(balls[i][0][1]*0.8+currentTime*0.3)*0.8):
            balls[i][1][1] -= 0.21
        balls[i][0][0] += balls[i][1][0]
        balls[i][0][1] += balls[i][1][1]

        if (balls[i][0][0] < 0):
            balls[i][1][0] = abs(balls[i][1][0])
            balls[i][0][0] = 0
        if (balls[i][0][0] > 32):
            balls[i][1][0] = -abs(balls[i][1][0])
            balls[i][0][0] = 32
        if (balls[i][0][1] < 0):
            balls[i][1][1] = abs(balls[i][1][0])
            balls[i][0][1] = 0
        if (balls[i][0][1] > 7):
            balls[i][1][1] = -abs(balls[i][1][0])
            balls[i][0][1] = 7

        matrix[math.floor(balls[i][0][0]), math.floor(balls[i][0][1])] = (255,0,0)
    matrix.show()
    time.sleep(0)
    current_frame += 1
    currentTime += 1
    if current_frame >= len(imgdata): current_frame = 0