import pixelstrip
import board
import time
import random
import math



class SandAnimation(pixelstrip.Animation):
	width: int
	height: int

	state: list[list[int]] = []
	next_state: list[list[int]] = []
 
	frame: int = 0
	full_timer: int = 0
	FPS: int
	new_spawn_chance: float = 1
	init_spawn_chance: float = 0.05
 
	colors: list[tuple[int]] = [(0, 0, 0), (20, 10, 0), (25, 12, 5), (5, 12, 7), (25, 25, 0), (21, 3, 15)]
	
	def __init__(self, FPS=10, new_spawn_chance=0.5, init_spawn_chance=0.05, width=8, height=8):
		pixelstrip.Animation.__init__(self)
		self.FPS = FPS
		self.new_spawn_chance = new_spawn_chance
		self.init_spawn_chance = init_spawn_chance
  
		self.width = width
		self.height = height

		self.init()
  
	def init(self):
		self.frame = 0
		self.full_timer = 0
		self.state.clear()
		self.next_state.clear()
		for _y in range(self.height):
			row = []
			for _x in range(self.width):
				row.append(random.randint(1,5) if random.random()<self.init_spawn_chance else 0)
			self.state.append(row.copy())
			self.next_state.append(row.copy())
	
	def update(self):
		if random.random()<self.new_spawn_chance:
			self.state[0][random.randint(0, self.width-1)] = random.randint(1,5)

		for y in range(self.height):
			for x in range(self.width):
				if self.state[y][x] != 0:
					if y >= self.height-1:
						continue
		
					y_under = mid(self.height-1, y+1, 0)
					x_left = mid(self.width-1, x-1, 0)
					x_right = mid(self.width-1, x+1, 0)
					
					tile_under = self.state[y_under][x] != 0
	
					if not tile_under:
						self.next_state[y][x] = 0
						self.next_state[y_under][x] = self.state[y][x]
					else: # tile under
						choice = x_left if random.random()<0.5 else x_right
						opposite_choice = x_right if choice==x_left else x_left
						if self.state[y_under][choice] == 0:
							self.next_state[y][x] = 0
							self.next_state[y_under][choice] = self.state[y][x]
						elif self.state[y_under][opposite_choice] == 0:
							self.next_state[y][x] = 0
							self.next_state[y_under][opposite_choice] = self.state[y][x]
		full: bool = True
		for y in range(self.height):
			for x in range(self.width):
				if y>0 and self.state[y][x] == 0:
					full = False
				self.state[y][x] = self.next_state[y][x]
		if full and self.full_timer < 10:
			self.full_timer += 1
		elif self.full_timer >= 10:
			self.init()
		self.frame+=1
		
	def reset(self, strip):
		strip.clear()
		strip.show()
		self.init()

	def draw(self, strip, delta_time):
		self.update()
		for y in range(self.height):
			for x in range(self.width):
				strip[x, y] = (mul_color_number(self.colors[mid(0, self.state[y][x], len(self.colors)-1)], abs(math.sin(self.frame))+1))
		strip.show()
		time.sleep(1 / self.FPS)
		# self.frame += 1



def mid(a, b, c):
	return max(min(a, b), min(max(a, b), c))

def mul_color_number(color: tuple[int], number: int):
	return (color[0] * number,
			color[1] * number,
			color[2] * number)

if __name__ == "__main__":

	width = 8
	height = 8
 
	pixel = pixelstrip.PixelStrip(
		board.GP15,
		width=width,
		height=height,
		bpp=4,
		pixel_order=pixelstrip.GRB,
		options={pixelstrip.MATRIX_COLUMN_MAJOR, pixelstrip.MATRIX_ZIGZAG},
		brightness=0.5
	)

	pixel.clear()

	pixel.animation = SandAnimation()
	while True:
		pixel.draw()

