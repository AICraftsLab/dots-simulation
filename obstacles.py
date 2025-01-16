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