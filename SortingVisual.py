import pixelstrip
import random
import math
from colors import *


class SortingVisualAnimation(pixelstrip.Animation):
	width: int
	height: int
	
	idx: int = 0

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
		self.idx = 0
		for i in range(self.width):
			self.numbers.append(math.floor(self.height*(i/self.width))+1)
		self.shuffle()

	def reset(self, strip):
		self.timeout = 1 / self.FPS
		self.init()
		strip.clear()

	def shuffle(self):
		for _ in range(50):
			first_idx = random.randint(1, len(self.numbers)) - 1
			second_idx = random.randint(1, len(self.numbers)) - 1
			if first_idx == second_idx:
				continue
			self.numbers[first_idx], self.numbers[second_idx] = self.numbers[second_idx], self.numbers[first_idx]
		print(self.numbers)
		
	def update(self):
		cur: int = self.numbers[self.idx]
		next: int = self.numbers[self.idx + 1]
		
		if cur > next:
			self.numbers[self.idx + 1] = cur
			self.numbers[self.idx] = next

		self.idx += 1
		self.idx %= len(self.numbers) - 1
  
		if self.idx == 0 and sorted(self.numbers) == self.numbers:
			self.reset({})


	def draw(self, strip, _delta_time):
		if self.is_timed_out():
			self.timeout = 1 / self.FPS
			
			self.update()

			# strip.clear()
			column_width: int = math.floor(self.width/self.height)
			for i in range(len(self.numbers)):
				for j in range(8):
					strip[i,j] = WHITE if j < self.numbers[i] else BLACK
			for j in range(abs(8 - self.numbers[self.idx])):
				strip[self.idx, abs(7-j)] = PURPLE
			
			strip.show()


