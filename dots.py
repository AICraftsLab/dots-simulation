import pygame as pg
import random
import pickle
import math
import os
import copy

pg.font.init()

GENERATIONS = 1500
WIDTH = 600
HEIGHT = 600
POPULATION = 500
MATING_POOL_SIZE = POPULATION // 10
MUTATION_PROB = 0.05
ELITISM = 15  # 3% of population
GOAL_SIZE = 10
GOAL_RADIUS = GOAL_SIZE // 2
GOAL_REWARD = 100
DOTS_XVEL = 15
DOTS_RADIUS = 3


def write_run_parameters(file, more_info=''):
    data = f'{WIDTH=}\n{HEIGHT=}\n{POPULATION=}\n{MATING_POOL_SIZE=}\n{MUTATION_PROB=}\n' \
           f'{ELITISM=}\n{GOAL_SIZE=}\n{GOAL_RADIUS=}\n{GOAL_REWARD=}\n{DOTS_XVEL=}\n' \
           f'{DOTS_RADIUS=}\n{GENERATIONS=}\n\n{more_info}\n\n'
           
    file.write(data)
    file.flush()

class Dot:
    VEL = pg.Vector2((DOTS_XVEL, 0))  # 3
    RADIUS = DOTS_RADIUS # 3
    LIVE_COLOR = 'green'
    DEAD_COLOR = 'gray'
    
    def __init__(self, position, moves=[]):
        self.position = pg.Vector2(position)
        self.directions = moves.copy()
        self.move_idx = 0
        self.alive = True
    
    def get_fitness(self, goal):
        distance_to_goal = math.dist(self.position, goal.rect.center)
        distance_score = GOAL_REWARD if distance_to_goal <= GOAL_RADIUS else -distance_to_goal
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
                if isinstance(obstacle, Goal):
                    if False and len(self.directions) - 1 > self.move_idx:
                        self.directions = self.directions[:self.move_idx]
                return True
        
        return False
    
    def draw(self, surface):
        if self.alive:
            pg.draw.circle(surface, self.LIVE_COLOR, self.position, self.RADIUS)
        else:
            pg.draw.circle(surface, self.DEAD_COLOR, self.position, self.RADIUS)
    
    @classmethod
    def crossover(cls, position, dot1, dot2):
        point = random.randrange(min(dot1.move_idx, dot2.move_idx))
        new_dot1_directions = []
        new_dot2_directions = []
        
        # Stopping at move_idx bcoz if, due to mutation, a dot died
        # or reached goal before following all its inherited genes,
        # then don't pass the genes not followed to the offspring
        # bcoz they are not required for reaching the goal or
        # a dot will likely die before following them.
        new_dot1_directions.extend(dot1.directions[:point])
        new_dot1_directions.extend(dot2.directions[point:dot1.move_idx])
        
        new_dot2_directions.extend(dot2.directions[:point])
        new_dot2_directions.extend(dot1.directions[point:dot1.move_idx])
        
        new_dot1 = Dot(position, new_dot1_directions)
        new_dot2 = Dot(position, new_dot2_directions)
        
        return new_dot1, new_dot2
        

class Population:
    def __init__(self, position, goal, size):
        self.position = position
        self.goal = goal
        self.dots = []
        self.size = size
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
            parents = random.sample(best_dots, k = 2)
            child1, child2 = Dot.crossover(self.position, *parents)
            
            child1.mutate(MUTATION_PROB)
            child2.mutate(MUTATION_PROB)
            
            new_population.append(child1)
            new_population.append(child2)
        
        for dot in best_dots:
            if dot.get_fitness(self.goal) >= GOAL_REWARD:
                reached_goal_dots += 1
            dot.reset(self.position)
            
        new_population.extend(best_dots[:ELITISM])
        
        self.__alive = len(new_population)
        self.dots = new_population
        
        return best_dot, best_dot_moves, reached_goal_dots
            
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
        
    def draw(self, surface):
        for dot in self.dots:
            dot.draw(surface)
    
    def select_best_dots(self, n):
        key = lambda x: x.get_fitness(self.goal)
        dots = sorted(self.dots, key=key, reverse=True)
        dots = dots[:n]
        
        return dots
    
    def alive(self):
        return self.__alive > 0
    
    def save(self, file):
        with open(file, 'w+b') as f:
            pickle.dump(self, f)
            
    @classmethod
    def load(cls, file):
        with open(file, 'r+b') as f:
            obj = pickle.load(f)
        return obj
       
       
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
        
    def __repr__(self):
        return str(self.rect)


class Goal(Obstacle):
    COLOR = 'red'
    
   
if __name__ == '__main__':
    window = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption('Dots Simulation')
    clock = pg.time.Clock()
    
    font = pg.font.SysFont('sanscomic', 35)
    
    run_dir = 'run3'
    save_files = True
    
    # Dots starting position
    position = (WIDTH // 2, HEIGHT * 0.9)
    goal = Goal(WIDTH // 2, 50, GOAL_SIZE, GOAL_SIZE)
    
    obstacles0 = [goal]
    obstacles1 = [
        goal,
        Obstacle(WIDTH * 0.75, HEIGHT * 0.25, 100, 20),
        Obstacle(WIDTH * 0.75, HEIGHT * 0.75, 100, 20),
        Obstacle(WIDTH * 0.25, HEIGHT * 0.25, 100, 20),
        Obstacle(WIDTH * 0.25, HEIGHT * 0.75, 100, 20),
        Obstacle(WIDTH // 2, HEIGHT // 2, 400, 20),
    ]
    
    obstacles2 = [
        goal,
        Obstacle(0, HEIGHT * 0.8, 400, 20, 'left'),
        Obstacle(WIDTH, HEIGHT * 0.6, 400, 20, 'right'),
        Obstacle(0, HEIGHT * 0.4, 400, 20, 'left'),
        Obstacle(WIDTH, HEIGHT * 0.2, 400, 20, 'right'),
    ]
    
    obstacles3 = [
        goal,
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
    
    obstacles = obstacles3
    
    if save_files:
        os.makedirs(run_dir, exist_ok=True)
        
        pop_file_path = os.path.join(run_dir, 'population')
        summary_file_path = os.path.join(run_dir, 'summary.txt')
        summary_file = open(summary_file_path, 'w')
        more_info = f"{position=}\n{goal=}\n{obstacles=}"
        write_run_parameters(summary_file, more_info=more_info)
    
    population = Population(position, goal, POPULATION)
    #population = Population.load(os.path.join('run3', 'population_1490'))
    
    for i in range(GENERATIONS):
        while population.alive():
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    quit()
                    
            population.update(WIDTH, HEIGHT, obstacles)
            
            window.fill('white')
            
            for obstacle in obstacles:
                obstacle.draw(window)
            
            population.draw(window)
            
            gen_text = font.render('Gen: ' + str(i), 1, 'black')
            window.blit(gen_text, (10, 10))
            
            pg.display.flip()
            clock.tick(60)
            
        gen_data = population.generate_next_generation()
        print('Generation:', i, 'Best moves:', gen_data[1], 'Reached Goal:', gen_data[2])
        
        if save_files and i % 10 == 0:
            population.save(f'{pop_file_path}_{i}')
            print('Generation:', i, 'Best moves:', gen_data[1], 'Reached Goal:', gen_data[2], file=summary_file, flush=True)
        
        # Last generation
        if  i + 1 == GENERATIONS:
            population.save(f'{pop_file_path}_{i+1}')
            print('Generation:', i+1, 'Best moves:', gen_data[1], 'Reached Goal:', gen_data[2], file=summary_file, flush=True)

    if save_files:
        summary_file.close()