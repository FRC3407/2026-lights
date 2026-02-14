import pixelstrip
import board
import time
import random
import math
from colors import *


class SortingVisualAnimation(pixelstrip.Animation):
	width: int
	height: int
	
	FPS: int
	
	number: list[int]
	
	def __init__(self, FPS=10, width=8, height=8):
		pixelstrip.Animation.__init__(self)
		self.FPS = FPS
		
		self.width = width
		self.height = height
		
		self.init()
		
	def init(self):
		self.numbers = []
		for i in range(self.height):
			self.numbers.append(i)
		
	def draw(self, strip, _delta_time):
		strip.clear()
		
		column_width: int = math.floor(self.width/self.height)
		for i in range(len(self.numbers)):
			number: int = self.numbers[i]
			strip.draw_rect(i*column_width, self.height, column_width, -number, True)
		strip[column_width,1] = PURPLE
		
		strip.show()
		time.sleep(1 / self.FPS)
		
		
		
		
	
