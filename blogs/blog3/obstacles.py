import pygame as pg
from constants import *

class Obstacle:
    COLOR = 'black'
    def __init__(self, x, y, width, height, pos='center'):
        if pos == 'center':
            x = x - width // 2
            y = y - height // 2
            self.rect = pg.Rect((x, y, width, height))
        elif pos == 'right':
            x = x - width
            self.rect = pg.Rect((x, y, width, height))
        elif pos == 'left':
            self.rect = pg.Rect((x, y, width, height))
        
    def draw(self, surface):
        pg.draw.rect(surface, self.COLOR, self.rect)
    
    def collides(self, dot):
        return self.rect.collidepoint(dot.position)


class Goal(Obstacle):
    COLOR = 'red'
    

GOAL = Goal(WIDTH // 2, 50, GOAL_SIZE, GOAL_SIZE)

OBSTACLES0 = [GOAL]

OBSTACLES1 = [
    GOAL,
    Obstacle(WIDTH // 2, HEIGHT // 2, 400, 20),
]

OBSTACLES2 = [
    GOAL,
    Obstacle(WIDTH // 2, HEIGHT * 0.3, 400, 20),
    Obstacle(WIDTH // 2, HEIGHT * 0.7, 400, 20),
]

OBSTACLES3 = [
    GOAL,
    Obstacle(WIDTH * 0.75, HEIGHT * 0.25, 100, 20),
    Obstacle(WIDTH * 0.75, HEIGHT * 0.75, 100, 20),
    Obstacle(WIDTH * 0.25, HEIGHT * 0.25, 100, 20),
    Obstacle(WIDTH * 0.25, HEIGHT * 0.75, 100, 20),
    Obstacle(WIDTH // 2, HEIGHT // 2, 400, 20),
]

OBSTACLES4 = [
    Obstacle(x, HEIGHT * y / 10, 50, 20, 'left')
    for x in range(0, 600, 60) for y in range(2, 9, 1)
]

OBSTACLES5 = [
    GOAL,
    Obstacle(0, HEIGHT * 0.7, 400, 20, 'left'),
    Obstacle(WIDTH // 2, HEIGHT // 2, 400, 20),
    Obstacle(WIDTH, HEIGHT * 0.3, 400, 20, 'right'),
]

OBSTACLES6 = [
    Obstacle(x, HEIGHT * y / 10, 50, 20, 'left')
    for x in range(0, 600, 65) for y in range(2, 7, 1)
]
OBSTACLES6.append(Obstacle(WIDTH // 2, HEIGHT * 0.75, 350, 20),)

OBSTACLES7 = [
    Obstacle(x + (25 if y % 2 == 0 else -5), HEIGHT * y / 10, 50, 20, 'left')
    for x in range(0, 600, 60) for y in range(2, 9, 1)
]

OBSTACLES8 = [
    Obstacle(x, HEIGHT * y / 10, 115, 20, 'left')
    for x in range(0, 600, 125) for y in range(2, 9, 2)
]
OBSTACLES8.extend(
    Obstacle(x, HEIGHT * y / 10, 63, 20, 'left')
    for x in range(0, 600, 73) for y in range(2, 9, 1)
    if y % 2 != 0
)

OBSTACLES9 = [
    Obstacle(0, HEIGHT * 0.2, WIDTH * 0.49, HEIGHT * 0.7, 'left'),
    Obstacle(WIDTH, HEIGHT * 0.2, WIDTH * 0.49, HEIGHT * 0.7, 'right')
]

OBSTACLES10 = [
    Obstacle(0, HEIGHT * 0.2, WIDTH * 0.3, HEIGHT * 0.63, 'left'),
    Obstacle(WIDTH * 0.32, HEIGHT * 0.2, WIDTH * 0.38, HEIGHT * 0.63, 'left'),
    Obstacle(WIDTH * 0.72, HEIGHT * 0.2, WIDTH * 0.3, HEIGHT * 0.63, 'left'),
]

OBSTACLES11 = [
    GOAL,
    Obstacle(0, HEIGHT * 0.8, 400, 20, 'left'),
    Obstacle(WIDTH, HEIGHT * 0.6, 400, 20, 'right'),
    Obstacle(0, HEIGHT * 0.4, 400, 20, 'left'),
]

OBSTACLES12 = [
    GOAL,
    Obstacle(0, HEIGHT * 0.8, 400, 20, 'left'),
    Obstacle(WIDTH, HEIGHT * 0.6, 400, 20, 'right'),
    Obstacle(0, HEIGHT * 0.4, 400, 20, 'left'),
    Obstacle(0, HEIGHT * 0.2, 50, 20, 'left'),
    Obstacle(60, HEIGHT * 0.2, 50, 20, 'left'),
    Obstacle(120, HEIGHT * 0.2, 50, 20, 'left'),
    Obstacle(180, HEIGHT * 0.2, 50, 20, 'left'),
    Obstacle(240, HEIGHT * 0.2, 50, 20, 'left'),
    Obstacle(300, HEIGHT * 0.2, 50, 20, 'left'),
    Obstacle(360, HEIGHT * 0.2, 50, 20, 'left'),
    Obstacle(420, HEIGHT * 0.2, 50, 20, 'left'),
    Obstacle(480, HEIGHT * 0.2, 50, 20, 'left'),
    Obstacle(540, HEIGHT * 0.2, 50, 20, 'left'),
    Obstacle(600, HEIGHT * 0.2, 50, 20, 'left'),
]

OBSTACLES13 = [
    GOAL,
    Obstacle(0, HEIGHT * 0.8, 400, 20, 'left'),
    Obstacle(WIDTH, HEIGHT * 0.6, 400, 20, 'right'),
    Obstacle(0, HEIGHT * 0.4, 400, 20, 'left'),
    Obstacle(WIDTH, HEIGHT * 0.2, 400, 20, 'right'),
]

OBSTACLES14A = [
    GOAL,
    Obstacle(0, HEIGHT * 0.8, 400, 20, 'left'),
    Obstacle(WIDTH, HEIGHT * 0.7, 400, 20, 'right'),
    Obstacle(0, HEIGHT * 0.6, 400, 20, 'left'),
    Obstacle(WIDTH, HEIGHT * 0.5, 400, 20, 'right'),
    Obstacle(0, HEIGHT * 0.4, 400, 20, 'left'),
    Obstacle(WIDTH, HEIGHT * 0.3, 400, 20, 'right'),
    Obstacle(0, HEIGHT * 0.2, 400, 20, 'left'),
]

OBSTACLES14B = [
    GOAL,
    Obstacle(0, HEIGHT * 0.8, 350, 20, 'left'),
    Obstacle(WIDTH, HEIGHT * 0.7, 350, 20, 'right'),
    Obstacle(0, HEIGHT * 0.6, 350, 20, 'left'),
    Obstacle(WIDTH, HEIGHT * 0.5, 350, 20, 'right'),
    Obstacle(0, HEIGHT * 0.4, 350, 20, 'left'),
    Obstacle(WIDTH, HEIGHT * 0.3, 350, 20, 'right'),
    Obstacle(0, HEIGHT * 0.2, 350, 20, 'left'),
]
