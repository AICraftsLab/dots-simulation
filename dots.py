import pygame as pg
import random
import math

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
POSITION = (WIDTH // 2, HEIGHT * 0.95)

class Dot:
    VEL = pg.Vector2((DOTS_XVEL, 0))
    RADIUS = DOTS_RADIUS
    LIVE_COLOR = 'green'
    DEAD_COLOR = 'gray'

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
        
    def draw(self, surface):
        if self.alive:
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
            dot.draw(surface)
    
    def generate_next_generation(self):
        new_population = []
        best_dots = self.select_best_dots(MATING_POOL_SIZE)
        best_dot = best_dots[0]
        best_dot_moves = best_dot.move_idx

        for _ in range(0, self.size - ELITISM):
            parent = random.choice(best_dots)
            child = parent.replicate()
            child.mutate()
            new_population.append(child)

        for dot in best_dots[:ELITISM]:        
            dot.reset()

        new_population.extend(best_dots[:ELITISM])

        self.__alive = len(new_population)
        self.elites = best_dots[:ELITISM]
        self.dots = new_population

        return best_dot, best_dot_moves
        
    def select_best_dots(self, n):
        key = lambda x: x.get_fitness(self.goal)
        dots = sorted(self.dots, key=key, reverse=True)
        dots = dots[:n]

        return dots
    
            
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
    window = pg.display.set_mode((WIDTH, HEIGHT))  # Creates the window
    pg.display.set_caption('Dots Simulation')  # Sets window's caption
    clock = pg.time.Clock()  # Clock for controlling fps
    font = pg.font.SysFont('comicsans', 20)  # font for creating texts

    goal = Goal(WIDTH // 2, 50, GOAL_SIZE, GOAL_SIZE)

    obstacles = [
        goal,
        Obstacle(WIDTH // 2, HEIGHT // 2, 400, 20),
    ]

    population = Population(goal, POPULATION)
        
    for i in range(GENERATIONS):
        while population.alive():
            # Handling window close event
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    quit()

            alive = population.update(obstacles)

            # Rendering objects
            window.fill('white')

            for obstacle in obstacles:
                obstacle.draw(window)

            population.draw(window)

            gen_text = font.render('Generation: ' + str(i), 1, 'black')
            window.blit(gen_text, (10, 10))

            alive_text = font.render('Alive: ' + str(alive), 1, 'black')
            window.blit(alive_text, (10, gen_text.get_height() + 10))

            # Update the display
            pg.display.flip()
            clock.tick(60)
        best, best_moves = population.generate_next_generation()
        print('Generation', i, 'Best dot moves', best_moves)
