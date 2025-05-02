from src.Food import Food
from src.Water import Water
from src.Bath import Bath
import numpy as np
import pygame


class Cage:
    def __init__(self, width, height, chickens, food_positions, water_positions, bath_positions):
        self.width = width
        self.height = height
        self.chickens = chickens
        self.food_sources = [Food(x, y) for x, y in food_positions]
        self.water_sources = [Water(x, y) for x, y in water_positions]
        self.bathing_areas = [Bath(x, y) for x, y in bath_positions]
        
        for chicken in self.chickens:
            chicken.set_cage(self)
        
        self.all_object_names = [f"chicken_{i}" for i in range(len(self.chickens))] + \
                [f"food_{i}" for i in range(len(self.food_sources))] +   \
                [f"water_{i}" for i in range(len(self.water_sources))] + \
                [f"bath_{i}" for i in range(len(self.bathing_areas))]
    
    def is_valid_position(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height
    
    def update(self):
        for chicken in self.chickens:
            chicken.act()
    
    def display_printed(self):
        grid = [['.' for _ in range(self.width)] for _ in range(self.height)]
        
        for food in self.food_sources:
            grid[food.y][food.x] = 'F'
        for water in self.water_sources:
            grid[water.y][water.x] = 'W'
        for bath in self.bathing_areas:
            grid[bath.y][bath.x] = 'B'
        for chicken in self.chickens:
            grid[chicken.y][chicken.x] = 'C'
        
        for row in grid:
            print(" ".join(row))
        print("\n")
    
    def interact(self, x, y):
        for food in self.food_sources:
            if food.x == x and food.y == y:
                return "food", food.consume()
        for water in self.water_sources:
            if water.x == x and water.y == y:
                return "water", water.consume()
        for bath in self.bathing_areas:
            if bath.x == x and bath.y == y:
                return "bath", bath.consume()
        
        return None, 0
    
    def get_adj_matr(self):
        # return the current adjacency matrix
        # so each chicken, consumeable gets the adjacent positions
        all_objects = self.chickens + self.food_sources + self.water_sources + self.bathing_areas
        num_objects = len(all_objects)
        
        # Initialize the adjacency matrix with zeros
        adj_matrix = [[0] * num_objects for _ in range(num_objects)]
        
        # Helper function to check if two objects are adjacent
        def is_adjacent(obj1, obj2):
            return abs(obj1.x - obj2.x) <= 1 and abs(obj1.y - obj2.y) <= 1
        
        # Fill the adjacency matrix
        for i in range(num_objects):
            for j in range(num_objects):
                if i != j and is_adjacent(all_objects[i], all_objects[j]):
                    adj_matrix[i][j] = 1
        
        return np.array(adj_matrix)

    def simulate(self, steps, adj_matrix_interval=None, visual=True):
        adj_matrices = []
        for step in range(steps):
            self.update()
            if visual:
                self.display_printed()
            if adj_matrix_interval and step % adj_matrix_interval == 0:
                adj_matrices.append(self.get_adj_matr())
        
        print("End report:")
        for chicken in self.chickens:
            #print the status of each chicken
            print(f"Chicken {chicken.id} \tFood: {chicken.food} \tWater: {chicken.water} \tClean: {chicken.clean}")

        return adj_matrices
    
    
    def simulate_visual(self, steps, adj_matrix_interval=None, visual=True):
        if visual:
            pygame.init()
            self.TILE_SIZE = 64  # or whatever size you want
            self.screen = pygame.display.set_mode((self.width * self.TILE_SIZE, self.height * self.TILE_SIZE))
            self.clock = pygame.time.Clock()

            # Load images
            surf_base = pygame.Surface((self.TILE_SIZE, self.TILE_SIZE))
            surf_base.fill((255, 255, 255))  # fill it white
            surf_food = pygame.Surface((self.TILE_SIZE, self.TILE_SIZE))
            surf_food.fill((200, 100, 100))
            surf_water = pygame.Surface((self.TILE_SIZE, self.TILE_SIZE))
            surf_water.fill((0, 0, 255))
            surf_bath= pygame.Surface((self.TILE_SIZE, self.TILE_SIZE))
            surf_bath.fill((0, 200, 100))
            self.IMAGES = {
                #'.': pygame.Surface((self.TILE_SIZE, self.TILE_SIZE)),  # blank tile
                #'F': pygame.image.load('food.png'),
                #'W': pygame.image.load('water.png'),
                #'B': pygame.image.load('bath.png'),
                #'C': pygame.image.load('chicken.png'),
                '.': surf_base,  # White empty
                'F': surf_food,      # Green food
                'W': surf_water,      # Blue water
                'B': surf_bath,    # Yellow bath
                'C': pygame.image.load('img/chicken_img.jpeg'),      #
            }
            for key in self.IMAGES:
                self.IMAGES[key] = pygame.transform.scale(self.IMAGES[key], (self.TILE_SIZE, self.TILE_SIZE))

        adj_matrices = []
        for step in range(steps):
            self.update()
            if visual:
                self.display()
            if adj_matrix_interval and step % adj_matrix_interval == 0:
                adj_matrices.append(self.get_adj_matr())
        
        print("End report:")
        for chicken in self.chickens:
            #print the status of each chicken
            print(f"Chicken {chicken.id} \tFood: {chicken.food} \tWater: {chicken.water} \tClean: {chicken.clean}")

        return adj_matrices
    
    def display(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        self.screen.fill((0, 0, 0))  # Clear screen

        grid = [['.' for _ in range(self.width)] for _ in range(self.height)]

        for food in self.food_sources:
            grid[food.y][food.x] = 'F'
        for water in self.water_sources:
            grid[water.y][water.x] = 'W'
        for bath in self.bathing_areas:
            grid[bath.y][bath.x] = 'B'
        for chicken in self.chickens:
            grid[chicken.y][chicken.x] = 'C'

        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                img = self.IMAGES.get(cell, self.IMAGES['.'])
                self.screen.blit(img, (x * self.TILE_SIZE, y * self.TILE_SIZE))

        pygame.display.flip()
        self.clock.tick(2)  # Control FPS