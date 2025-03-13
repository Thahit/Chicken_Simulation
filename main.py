from src.Cage import Cage
from src.Chicken import RandomChicken
import random

height = 10
width = 10

chickens = [RandomChicken(random.randint(0, width-1), random.randint(0, height-1)) for _ in range(5)]
cage = Cage(width=width, height=height, chickens=chickens, food_positions=[(0, 2), (0, 3)], water_positions=[(9, 1)], bath_positions=[(5, 9)])
for _ in range(10):  # Run 10 steps of the simulation
    cage.update()
    cage.display()

for chicken in chickens:
    print(chicken.id, chicken.food, chicken.water, chicken.clean,)

print(cage.get_adj_matr())
