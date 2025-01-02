import pygame as pg
import random
import math
import copy

pg.font.init()

GENERATIONS = 1000
WIDTH = 600
HEIGHT = 600
POPULATION = 500
MATING_POOL_SIZE = POPULATION // 10
MUTATION_PROB = 0.05
ELITISM = 15
GOAL_SIZE = 10
GOAL_RADIUS = GOAL_SIZE // 2
GOAL_REWARD = 100
DOTS_XVEL = 5
DOTS_RADIUS = 3
POSITION = WIDTH // 2, HEIGHT // 2


class Dot:
    VEL = pg.Vector2((DOTS_XVEL, 0))
    RADIUS = DOTS_RADIUS
    LIVE_COLOR = 'green'
    DEAD_COLOR = 'gray'
    
    def __init__(self, position, moves=None):
        self.position = pg.Vector2(position)
        self.directions = [] if moves is None else moves
        self.move_idx = 0
        self.alive = True
        
    def move(self):
        if self.move_idx < len(self.directions):
            direction = self.directions[self.move_idx]
        else:
            direction = self.VEL.rotate(random.randrange(360))
            self.directions.append(direction)
        
        self.position += direction
        self.move_idx += 1
    
    def draw(self, surface):
        if self.alive:
            pg.draw.circle(surface, self.LIVE_COLOR, self.position, self.RADIUS)
        else:
            pg.draw.circle(surface, self.DEAD_COLOR, self.position, self.RADIUS)
            

if __name__ == '__main__':
    window = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption('Dots Simulation')
    clock = pg.time.Clock()
    font = pg.font.SysFont('comicsans', 20)
    
    for i in range(GENERATIONS):
        dot = Dot(POSITION)
        while dot.alive:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    quit()
                    
            dot.move()
            
            if dot.position.x < 0 or dot.position.x > WIDTH or \
                   dot.position.y < 0 or dot.position.y > HEIGHT:
                dot.alive = False
            
            
            window.fill('white')
            dot.draw(window)
            
            gen_text = font.render('Generation: ' + str(i), 1, 'black')
            window.blit(gen_text, (10, 10))
            
            pg.display.flip()
            clock.tick(60)
        print('Generation', i, dot.move_idx, dot.directions[:3])
            