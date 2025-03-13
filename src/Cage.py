from src.Food import Food
from src.Water import Water
from src.Bath import Bath
import numpy as np

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
    
    def is_valid_position(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height
    
    def update(self):
        for chicken in self.chickens:
            chicken.act()
    
    def display(self):
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