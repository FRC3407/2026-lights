import pixelstrip
import board

import time

import sort_animation as sortanim, sort as algorithms

width: int = 8
height: int = 8



pixel = pixelstrip.PixelStrip(
    board.GP15,
    width=32,
    height=8,
    bpp=4,
    pixel_order=pixelstrip.GRB,
    options={pixelstrip.MATRIX_COLUMN_MAJOR, pixelstrip.MATRIX_ZIGZAG},
    brightness=0.015
)
pixel.animation = sortanim.SortAnimation(algorithms.AmericaSort, width, height, fps=30)

pixel.clear()

while True:
    pixel.animation.sorter.done = 0
    pixel.animation.sorter.verified = False
    pixel.animation.sorter.reroll()
    while pixel.animation.sorter.done <= 2:
        pixel.draw()
    
    time.sleep(0.5)