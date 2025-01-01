import pygame as pg
import random
import math
import copy

pg.font.init()


GENERATIONS = 3000
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

# Dots starting position
POSITION = (WIDTH // 2, HEIGHT * 0.95)


class Dot:
    VEL = pg.Vector2((DOTS_XVEL, 0))
    RADIUS = DOTS_RADIUS
    LIVE_COLOR = 'green'
    DEAD_COLOR = 'gray'
    
    def __init__(self, position, moves=[]):
        self.position = pg.Vector2(position)
        self.directions = moves.copy()
        self.move_idx = 0
        self.alive = True
    
    def get_fitness(self, goal):
        distance_to_goal = math.dist(self.position, goal.rect.center)
        distance_score = GOAL_REWARD if distance_to_goal <= GOAL_RADIUS + DOTS_RADIUS else -distance_to_goal
        fitness = distance_score + (1 / self.move_idx)
        return fitness
    
    def reset(self, position):
        self.move_idx = 0
        self.position = position
        self.alive = True
    
    def mutate(self, prob):
        for i in range(len(self.directions)):
            if random.random() < prob:
                direction = Dot.VEL.rotate(random.randrange(360))
                self.directions[i] = direction
    
    def move(self):
        if self.move_idx < len(self.directions):
            direction = self.directions[self.move_idx]
        else:
            direction = self.VEL.rotate(random.randrange(360))
            self.directions.append(direction)
        
        self.position += direction
        self.move_idx += 1
    
    def collides(self, obstacles):
        for obstacle in obstacles:
            if obstacle.collides(self):
                return True
        
        return False
    
    def draw(self, surface):
        if self.alive:
            pg.draw.circle(surface, self.LIVE_COLOR, self.position, self.RADIUS)
        else:
            pg.draw.circle(surface, self.DEAD_COLOR, self.position, self.RADIUS)
    
    def replicate():
        return Dot(self.directions)
        

class Population:
    def __init__(self, position, goal, size):
        self.position = position
        self.goal = goal
        self.dots = []
        self.size = size
        self.elites = []
        self.__alive = size
        
        self.__populate()
         
    def __populate(self):
        for _ in range(self.size):
            dot = Dot(self.position)
            self.dots.append(dot)
    
    def generate_next_generation(self):
        new_population = []
        best_dots = self.select_best_dots(MATING_POOL_SIZE)
        best_dot = best_dots[0]
        best_dot_moves = best_dot.move_idx
        reached_goal_dots = 0
        
        for _ in range(0, self.size - ELITISM, 2):
            parents = random.choices(best_dots, k = 2)
            child1, child2 = Dot.crossover(self.position, *parents)
            
            child1.mutate(MUTATION_PROB)
            child2.mutate(MUTATION_PROB)
            
            new_population.append(child1)
            new_population.append(child2)
        
        for dot in best_dots:
            dot.reset(self.position)
            
        new_population.extend(best_dots[:ELITISM])
        
        self.__alive = len(new_population)
        self.dots = new_population
        
        return best_dot, best_dot_moves
        
    def update(self, width, height, obstacles):
        alive = 0
        for dot in self.dots:
            if dot.alive:
                alive += 1
                dot.move()
                
                if dot.position.x < 0 or dot.position.x > width or \
                   dot.position.y < 0 or dot.position.y > height or \
                   dot.collides(obstacles):
                    dot.alive = False
        
        self.__alive = alive
        return alive
        
    def draw(self, surface):
        for dot in self.dots:
            if dot in self.elites:
                dot.draw(surface, True)
            else:
                dot.draw(surface)
    
    def select_best_dots(self, n):
        key = lambda x: x.get_fitness(self.goal)
        dots = sorted(self.dots, key=key, reverse=True)
        dots = dots[:n]
        
        return dots
    
    def alive(self):
        return self.__alive > 0


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






if __name__ == '__main__':
    window = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption('Dots Simulation')
    clock = pg.time.Clock()
    
    font = pg.font.SysFont('comicsans', 20)
    
    GOAL = Goal(WIDTH // 2, 50, GOAL_SIZE, GOAL_SIZE)

    OBSTACLES0 = [GOAL]

    OBSTACLES1 = [
        GOAL,
        Obstacle(WIDTH // 2, HEIGHT // 2, 400, 20),
    ]
    
    obstacles = OBSTACLES0
    population = Population(POSITION, GOAL, POPULATION)
    
    for i in range(GENERATIONS):
        while population.alive():
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    quit()
                    
            alive = population.update(WIDTH, HEIGHT, obstacles)
            window.fill('white')
            
            for obstacle in obstacles:
                obstacle.draw(window)
            
            population.draw(window)
            
            gen_text = font.render('Generation: ' + str(i), 1, 'black')
            window.blit(gen_text, (10, 10))
            
            alive_text = font.render('Alive: ' + str(alive), 1, 'black')
            window.blit(alive_text, (10, gen_text.get_height() + 10))
            
            pg.display.flip()
            clock.tick(60)
            
        gen_data = population.generate_next_generation()
        print('Generation:', i, 'Best moves:', gen_data[1])