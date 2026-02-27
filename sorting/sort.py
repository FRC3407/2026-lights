import random
import math

def random_sample_recreation(population, k):
    if k < 0 or k > len(population):
        raise ValueError("Sample size k must be between 0 and the population size")

    # Work with a copy to avoid modifying the original list
    temp_population = list(population)
    result = []

    for _ in range(k):
        # Pick a random index from the remaining population
        random_index = random.randrange(len(temp_population))

        # Append the item at that index to the result
        result.append(temp_population.pop(random_index))

    return result

class Sort:
    def __init__(self, w, h):
        randarr: list[float] = [random.random() for i in range(w)]
        roundarr: list[int] = list(map(lambda x : round(x*h), randarr))
        self.arr: list[int] = roundarr
        
        self.width: int = w
        self.height: int = h
        self.pos: int = 0
        self.lastpos: int = 0
        
        self.verified: bool = True
        self.done: int = 0
    
    def reroll(self):
        randarr: list[float] = [random.random() for i in range(self.width)]
        roundarr: list[int] = list(map(lambda x : round(x*self.height), randarr))
        self.arr = roundarr
    
    def step(self):
        self.verified = self.arr == sorted(self.arr)
    
    def draw(self, matrix):
        if self.done >= 2: return
        
        matrix.npxl.fill((0, 0, 0))
        
        arrlen = len(self.arr)
        for i in range(arrlen):
            color = (255, 255, 255)
            
            if self.done >= 1:
                if i <= self.pos: color = (0, 255, 0)
                if self.pos <= self.lastpos:
                    self.pos += 1
                    self.lastpos = self.pos
            
            val = self.arr[i]
            for y in range(self.height):
                matrix[arrlen-i-1, y] = (color if y <= val else (0, 0, 0))

class StepSort(Sort):
    def draw(self, matrix):
        Sort.draw(self, matrix)
        
        arrlen: int = len(self.arr)
        color = (0, 255, 0)
            
        val = self.arr[self.pos]
        for y in range(self.height):
            matrix[arrlen-self.pos-1, y] = color if y <= val else (0, 0, 0)
    
    def step(self):
        Sort.step(self)
        
        if self.pos < len(self.arr) - 1:
            self.process()
            self.pos += 1
        else:
            self.pos = 0
            if self.verified:
                self.done += 1

    def process(self):
        pass


# ================================ SORT MAKING !!! ================================ #

class BubbleSort(StepSort):
    def process(self):
        current: int = self.arr[self.pos]
        test: int = self.arr[self.pos+1]
        
        if test < current:
            self.arr[self.pos+1] = current
            self.arr[self.pos] = test

class QuickSort(Sort):
    def __init__(self, w, h):
        Sort.__init__(self, w, h)
        
        self.lo = 0
        self.hi = len(self.arr) - 1
    
    def draw(self, matrix):
        Sort.draw(self, matrix)
        
        
    
    def step(self):
        pass



# ================================ JOKE SORTS ================================ #

class StalinSort(StepSort):
    def process(self):
        current: int = self.arr[self.pos]
        test: int = self.arr[self.pos+1]
        
        if test < current:
            self.arr.pop(self.pos+1)

class IngsocSort(StepSort):
    def process(self):
        current: int = self.arr[self.pos]
        test: int = self.arr[self.pos+1]
        
        diff: int = test - current
        if diff < -3:
            self.arr.pop(self.pos+1)
        elif diff < 0:
            self.arr[self.pos+1] += 1

class MiracleSort(Sort):
    def step(self):
        if self.verified:
            self.done += 1

class GaslightSort(Sort):
    def step(self):
        self.done = 1

class BogoSort(Sort):
    def step(self):
        self.arr = random_sample_recreation(self.arr, len(self.arr))
        if self.verified:
            self.done += 1
            self.pos = 0
        else:
            self.pos = -1

class SortSort(StepSort):
    def __init__(self, w, h):
        Sort.__init__(self, w, h)
        
        self.newarr = []
        self.target = 0
        self.compensate = 0
    
    def draw(self, matrix):
        StepSort.draw(self, matrix)
    
    def process(self):
        if self.pos == 0: self.compensate = 0
        i: int = self.pos-self.compensate
        
        if self.arr[self.pos] == self.target:
            self.newarr.append(self.arr.pop(i))
            self.compensate += 1
            return
        
        if self.newarr == sorted(self.newarr):
            self.arr.append(self.newarr[i])
            self.compensate += 1

class DarwinSort(Sort):
    def step(self):
        Sort.step(self)




SORTS: list[type[Sort]] = [
    BubbleSort,
    QuickSort,
    StalinSort,
    IngsocSort
]

class AmericaSort(Sort):
    def __init__(self, w, h):
        Sort.__init__(self, w, h)
        
        self.president: type[Sort] = MiracleSort
        self.year = 1
    
    def step(self):
        Sort.step(self)
        
        if self.year % 4 == 0:
            candidates: list[type[Sort]] = random_sample_recreation(SORTS, 2)
            
            results: list[int] = self.hold_vote()
            while results[0] == results[1]:
                results = self.hold_vote()
            
            winner: type[Sort] = candidates[int(results[0] > results[1])]
            self.president = winner
        
        self.president.step(self)
        self.year += 1
    
    def hold_vote(self) -> list[int]:
        votes: list[int] = list(map(lambda x : round(random.random()), self.arr))
        
        votecount: list[int] = [0, 0]
        for vote in votes: votecount[vote] += 1
        
        return votecount