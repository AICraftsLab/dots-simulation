import pygame as pg
import random
import pickle
import math
import os
import copy
from constants import *
from obstacle import *

pg.font.init()


def write_run_parameters(file, more_info=''):
    data = f'{WIDTH=}\n{HEIGHT=}\n{POPULATION=}\n{MATING_POOL_SIZE=}\n{MUTATION_PROB=}\n' \
           f'{ELITISM=}\n{GOAL_SIZE=}\n{GOAL_RADIUS=}\n{GOAL_REWARD=}\n{DOTS_XVEL=}\n' \
           f'{DOTS_RADIUS=}\n{GENERATIONS=}\n{POSITION=}\n{GOAL=}\n\n\n{more_info}\n\n'
           
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
        new_dot1_directions.extend(dot2.directions[point:dot2.move_idx])
        
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
            parents = random.choices(best_dots, k = 2)
            child1, child2 = Dot.crossover(self.position, *parents)
            
            child1.mutate(MUTATION_PROB)
            child2.mutate(MUTATION_PROB)
            
            new_population.append(child1)
            new_population.append(child2)
        
        for dot in self.dots:
            if dot.get_fitness(self.goal) >= GOAL_REWARD:
                reached_goal_dots += 1
        
        for dot in best_dots:        
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
        return alive
        
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
           
   
if __name__ == '__main__':    
    window = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption('Dots Simulation')
    clock = pg.time.Clock()
    
    font = pg.font.SysFont('comicsans', 20)
    
    run_dir = 'run1'
    save_files = True
    obstacles = OBSTACLES1
    
    if GOAL not in obstacles:
        obstacles.append(GOAL)
    
    if save_files:
        os.makedirs(run_dir, exist_ok=True)
        
        pop_file_path = os.path.join(run_dir, 'population')
        summary_file_path = os.path.join(run_dir, 'summary.txt')
        summary_file = open(summary_file_path, 'w')
        more_info = f"{obstacles=}"
        write_run_parameters(summary_file, more_info=more_info)
    
    population = Population(POSITION, GOAL, POPULATION)
    #population = Population.load(os.path.join('r14g_O14_vel15_changed', 'population_9000'))
    reached_goal = 0
    render = True
    
    for i in range(GENERATIONS):
        while population.alive():
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    quit()
                    
                if e.type == pg.MOUSEBUTTONDOWN:
                    render = not render
                    
            alive = population.update(WIDTH, HEIGHT, obstacles)
            window.fill('white')
            
            if render:
                for obstacle in obstacles:
                    obstacle.draw(window)
                
                population.draw(window)
            
            gen_text = font.render('Generation: ' + str(i), 1, 'black')
            window.blit(gen_text, (10, 10))
            
            alive_text = font.render('Alive: ' + str(alive), 1, 'black')
            window.blit(alive_text, (10, gen_text.get_height() + 10))
            
            reached_goal_text = font.render('Reached: ' + str(reached_goal), 1, 'black')
            window.blit(reached_goal_text, (10, alive_text.get_height() * 2 + 10))
            
            pg.display.flip()
            if render:
                clock.tick(60)
            
        gen_data = population.generate_next_generation()
        reached_goal = gen_data[2]
        print('Generation:', i, 'Best moves:', gen_data[1], 'Reached Goal:', reached_goal)
        
        if save_files and i % 10 == 0:
            population.save(f'{pop_file_path}_{i}')
            print('Generation:', i, 'Best moves:', gen_data[1], 'Reached Goal:', gen_data[2], file=summary_file, flush=True)
        
        # Last generation
        if save_files and i + 1 == GENERATIONS:
            population.save(f'{pop_file_path}_{i+1}')
            print('Generation:', i+1, 'Best moves:', gen_data[1], 'Reached Goal:', gen_data[2], file=summary_file, flush=True)

    if save_files:
        summary_file.close()