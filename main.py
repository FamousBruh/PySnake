import threading
from os import system
from random import randint
from keyboard import is_pressed

class Game:
    def __init__(self):
        self.grid = [["-"]*25 for i in range(25)]
        self.body = [[12, 3]]
        self.size = 1
        self.score = 0
        self.fruit = False
        self.fruit_x = 0
        self.fruit_y = 0
        self.fruit_pos = []
        self.movement = [1, 0] # Written as an x and y per frame, grid is a coordinate with flipped y axis (0, 1 is down)
        self.previous = []
    
    def move(self):
        self.next_x = self.body[-1:][0][0]
        self.next_y = self.body[-1:][0][1]
        self.next = [(self.body[-1:][0][0] + self.movement[1])%25, (self.body[-1:][0][1] + self.movement[0])%25]
        for chunk in self.body:
            if(chunk == self.next):
                return 0
        self.body.append(self.next)
        temp_x = self.body[0][0]
        temp_y = self.body[0][1]
        self.grid[temp_x][temp_y] = "-"
        self.previous = self.body[0]
        self.body.pop(0)
        if(self.body[-1:][0][0] == self.fruit_x and self.body[-1:][0][1] == self.fruit_y):
            self.fruit = False
            self.make_bigger()
    
    def spawn_fruit(self):
        try:
            invalid = ["-", "#"]
            self.fruit_x = randint(0, 24)
            self.fruit_y = randint(0, 24)
            while(self.grid[self.fruit_x][self.fruit_y] not in invalid):
                self.fruit_x = randint(0, 14)
                self.fruit_y = randint(0, 14)
            self.grid[self.fruit_x][self.fruit_y] = "o"
        except:
            pass

    def make_bigger(self):
        self.size += 1
        self.score += 1
        snake_body = [self.previous] + self.body
        self.body = snake_body

    def print_grid(self):
        try:
            system("CLS")
        except:
            system("clear")
        self.update_grid()
        for x in range(0, 25):
            for y in range(0, 25):
                print(self.grid[x][y], end = "")
            print()
        print("Size:", self.size)
        print("Score:", self.score)

    def update_grid(self):
        if(self.fruit == False):
            self.fruit = True
            self.spawn_fruit()
        for item in self.body:
            self.grid[item[0]][item[1]] = "#"

def setInterval(func,time):
    e = threading.Event()
    while not e.wait(time):
        func()

def update():
    try:
        if(is_pressed("a") or is_pressed("left")):
            game.movement = [-1, 0]
        if(is_pressed("s") or is_pressed("down")):
            game.movement = [0, 1]
        if(is_pressed("w") or is_pressed("up")):
            game.movement = [0, -1]
        if(is_pressed("d") or is_pressed("right")):
            game.movement = [1, 0]
    except:
        pass
    game.move()
    game.print_grid()

game = Game()
setInterval(update, 0.1)
