#import pygame as pg
import random
import math
import pickle
import os
from obstacles import *

pg.font.init()

class Dot:
    VEL = pg.Vector2((DOTS_XVEL, 0))
    RADIUS = DOTS_RADIUS
    LIVE_COLOR = 'green'
    DEAD_COLOR = 'gray'
    ELITES_COLOR = 'blue'

    def __init__(self, moves=None):
        self.position = pg.Vector2(POSITION)
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
        
    def draw(self, surface, is_elite=False):
        if is_elite:
            pg.draw.circle(surface, self.ELITES_COLOR, self.position, self.RADIUS)
        elif self.alive:
            pg.draw.circle(surface, self.LIVE_COLOR, self.position, self.RADIUS)
        else:
            pg.draw.circle(surface, self.DEAD_COLOR, self.position, self.RADIUS)
        
    def collides(self, obstacles):
        for obstacle in obstacles:
            if obstacle.collides(self):
                return True

        return False
        
    def get_fitness(self, goal):
        distance_to_goal = math.dist(self.position, goal.rect.center)
        distance_score = GOAL_REWARD if distance_to_goal <= GOAL_RADIUS + DOTS_RADIUS else -distance_to_goal
        fitness = distance_score + (1 / self.move_idx)
        return fitness

    def replicate(self):
        return Dot(self.directions.copy())

    def mutate(self):
        for i in range(len(self.directions)):
            if random.random() < MUTATION_PROB:
                direction = Dot.VEL.rotate(random.randrange(360))
                self.directions[i] = direction

    def reset(self):
        self.move_idx = 0
        self.position = pg.Vector2(POSITION)
        self.alive = True
        
    @classmethod
    def crossover(cls, parent1, parent2):
        point = random.randrange(min(parent1.move_idx, parent2.move_idx))
        offspring1_directions = []
        offspring2_directions = []
        
        offspring1_directions.extend(parent1.directions[:point])
        offspring1_directions.extend(parent2.directions[point:parent2.move_idx])
        
        offspring2_directions.extend(parent2.directions[:point])
        offspring2_directions.extend(parent1.directions[point:parent1.move_idx])
        
        offspring1 = Dot(offspring1_directions)
        offspring2 = Dot(offspring2_directions)
        
        return offspring1, offspring2
                

class Population:
    def __init__(self, goal, size):
        self.goal = goal
        self.size = size
        self.dots = []
        self.elites = []
        self.__alive = size

        self.__populate()

    def __populate(self):
        for _ in range(self.size):
            dot = Dot()
            self.dots.append(dot)
            
    def update(self, obstacles):
        alive = 0
        for dot in self.dots:
            if dot.alive:
                alive += 1
                dot.move()

                # Kill dots on going out of window's boundary or colliding with an obstacle
                if dot.position.x < 0 or dot.position.x > WIDTH or \
                   dot.position.y < 0 or dot.position.y > HEIGHT or \
                   dot.collides(obstacles):
                    dot.alive = False

        self.__alive = alive
        return alive
        
    def alive(self):
        return self.__alive > 0
        
    def draw(self, surface):
        for dot in self.dots:
            if dot in self.elites:
                dot.draw(surface, True)
            else:
                dot.draw(surface)
    
    def generate_next_generation(self):
        new_population = []
        best_dots = self.select_best_dots(MATING_POOL_SIZE)
        best_dot = best_dots[0]
        best_dot_moves = best_dot.move_idx
        reached_goal_dots = 0

        for _ in range(0, self.size - ELITISM, 2):
            parents = random.choices(best_dots, k = 2)
            child1, child2 = Dot.crossover(*parents)
            
            child1.mutate()
            child2.mutate()
            
            new_population.append(child1)
            new_population.append(child2)
        
        for dot in self.dots:
            if dot.get_fitness(self.goal) >= GOAL_REWARD:
                reached_goal_dots += 1
        
        for dot in best_dots[:ELITISM]:        
            dot.reset()

        new_population.extend(best_dots[:ELITISM])

        self.__alive = len(new_population)
        self.elites = best_dots[:ELITISM]
        self.dots = new_population

        return best_dot, best_dot_moves, reached_goal_dots
        
    def select_best_dots(self, n):
        key = lambda x: x.get_fitness(self.goal)
        dots = sorted(self.dots, key=key, reverse=True)
        dots = dots[:n]

        return dots
        
    def save(self, file):
        with open(file, 'w+b') as f:
            pickle.dump(self, f)
            
    @staticmethod
    def load(file):
        with open(file, 'r+b') as f:
            obj = pickle.load(f)
        return obj


if __name__ == '__main__':
    window = pg.display.set_mode((WIDTH, HEIGHT))  # Creates the window
    pg.display.set_caption('Dots Simulation')  # Sets window's caption
    clock = pg.time.Clock()  # Clock for controlling fps
    font = pg.font.SysFont('comicsans', 20)  # font for creating texts

    obstacles = OBSTACLES14B
    run_dir = 'run1'
    save_files = True
    render_objects = True
    
    if save_files:
        os.makedirs(run_dir)
        pop_file_path = os.path.join(run_dir, 'population')
    
    if GOAL not in obstacles:
        obstacles.append(GOAL)
    
    population = Population(GOAL, POPULATION)
    #population = Population.load('run1/population_100')
    reached_goal = 0
    
    for i in range(GENERATIONS):
        while population.alive():
            for e in pg.event.get():
                # Handling window close event
                if e.type == pg.QUIT:
                    pg.quit()
                    quit()
                elif e.type == pg.MOUSEBUTTONDOWN:  # Handling mouse/screen click
                    render_objects = not render_objects

            alive = population.update(obstacles)
            
            # If render_objects is set to true
            if render_objects:
                # Rendering all objects
                window.fill('white')

                for obstacle in obstacles:
                    obstacle.draw(window)

                population.draw(window)

                gen_text = font.render('Generation: ' + str(i), 1, 'black')
                window.blit(gen_text, (10, 10))

                alive_text = font.render('Alive: ' + str(alive), 1, 'black')
                window.blit(alive_text, (10, gen_text.get_height() + 10))

                reached_goal_text = font.render('Reached: ' + str(reached_goal), 1, 'black')
                window.blit(reached_goal_text, (10, alive_text.get_height() * 2 + 10))
                
                # Update the display
                pg.display.flip()
                clock.tick(60)  # Limit frames to 60 per second
            
        best, best_moves, reached_goal = population.generate_next_generation()
        print('Generation', i, 'Best dot moves', best_moves, 'Reached Goal:', reached_goal)
        
        # If render_objects is set to false
        if not render_objects:
            # Rendering only texts
            window.fill('white')
            
            gen_text = font.render('Generation: ' + str(i), 1, 'black')
            window.blit(gen_text, (10, 10))
            
            reached_goal_text = font.render('Reached: ' + str(reached_goal), 1, 'black')
            window.blit(reached_goal_text, (10, gen_text.get_height() + 10))
            
            # Update the display. Frames not limited
            pg.display.flip()
        
        # Save population after every 10 generations
        if save_files and i % 10 == 0:
            population.save(f'{pop_file_path}_{i}')
