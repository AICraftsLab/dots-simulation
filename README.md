Dots Evolution Simulation Program

Uses Simple Genetic Algorithm to evolve dots to move to a target position. The chromosome is a list of direction vectors that define the path taken (or to be taken) by a genome (dot).

*dots.py* is the main file. *dots_render.py* is developed to help me speed up the evolution process by toggling `rendering` ON/OFF on clicking the window. When `render` is OFF, dots and obstacles are not rendered and the framerate is not limited.

Feel free to tune these hyperparametes because they drive the evolution process:
1. MUTATION_PROB
2. MATING_POOL_SIZE
3. ELITISM

Looking forward to add BRAIN to the dots using NEAT and discard the chromosome thing.
