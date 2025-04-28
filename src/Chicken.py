import random
from src.GridObject import GridObject
from src.Cage import Cage
from abc import ABC


class Chicken(GridObject, ABC):
    _id_counter = 0
    def __init__(self, x, y, cage=None):
        super().__init__(x, y)
        self.cage: Cage = cage
        self.food = 100
        self.water = 1000
        self.clean = 100
        self.id = Chicken._id_counter
        Chicken._id_counter += 1
    
    def set_cage(self, cage: Cage):
        self.cage = cage
    
    def move(self):
        pass  # Abstract move method for different chicken types
    
    def act(self):
        self.move()
        
        self.interact()
    
    def interact(self):
        # eat/drink... if in the correct position
        interaction_type, value = self.cage.interact(self.x, self.y)

        if interaction_type == "food":#eat
            self.food += value
        elif interaction_type == "water":#drink 
            self.water += value
        elif interaction_type == "bath":#bath
            self.clean += value
    
    def get_objects_in_range(self, objects):
        return [obj for obj in objects if abs(obj.x - self.x) <= 1 and abs(obj.y - self.y) <= 1]

    def percept(self):
        #like a cellular automata, look around 1 range

        chickens = self.get_objects_in_range(self.cage.chickens)
        food = self.get_objects_in_range(self.cage.food_sources)
        water = self.get_objects_in_range(self.cage.water_sources)
        bath = self.get_objects_in_range(self.cage.bathing_areas)
        return chickens, food, water
        
    def consume_energy(self):
        self.food -=1
        self.water -=1

class RandomChicken(Chicken):
    def move(self):
        dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)])  # Allow standing still
        new_x, new_y = self.x + dx, self.y + dy
        
        if self.cage and self.cage.is_valid_position(new_x, new_y):
            self.x, self.y = new_x, new_y
        
        # energy cost
        self.consume_energy()



import numpy as np
import random

class WeightedRandomChicken(Chicken):
    def __init__(self, x, y, cage=None):
        super().__init__(x, y, cage)
        
        # Initialize grid that tracks how long ago she was in each place
        self.past_positions_grid = np.full((self.cage.height, self.cage.width), -1, dtype=int)
        
        # Initialize coordinates for food, water, and bath
        self.food_coords = [(food.x, food.y) for food in self.cage.food_sources]
        self.water_coords = [(water.x, water.y) for water in self.cage.water_sources]
        self.bath_coords = [(bath.x, bath.y) for bath in self.cage.bathing_areas]



def move(self):
    possible_moves = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]  # Including stay still
    move_scores = []
    
    # Parameters
    memory_decay = 10  # How quickly chicken "forgets" visited locations
    base_random_weight = 1.0  # Base weight for randomness
    
    # Calculate need levels (higher value = greater need)
    hunger_need = max(0, (100 - self.hunger) / 100)  # 0 when full, 1 when starving
    thirst_need = max(0, (100 - self.thirst) / 100)  # 0 when not thirsty, 1 when very thirsty
    cleanliness_need = max(0, (100 - self.cleanliness) / 100)  # 0 when clean, 1 when dirty
    
    # Need weights - how much each need influences decisions
    hunger_weight = 3.0
    thirst_weight = 3.5  # Slightly more important than hunger
    cleanliness_weight = 2.0  # Less critical than food/water
    
    # Calculate scores for each possible move
    for dx, dy in possible_moves:
        new_x, new_y = self.x + dx, self.y + dy
        
        # Skip invalid moves
        if not self.cage or not self.cage.is_valid_position(new_x, new_y):
            move_scores.append(0)
            continue
        
        # Start with base random score
        score = base_random_weight
        
        # Check if new position contains resources
        new_pos = (new_x, new_y)
        
        # Add attraction to food based on hunger
        if new_pos in self.food_coords:
            score += hunger_need * hunger_weight
        
        # Add attraction to water based on thirst
        if new_pos in self.water_coords:
            score += thirst_need * thirst_weight
        
        # Add attraction to bath based on cleanliness need
        if new_pos in self.bath_coords:
            score += cleanliness_need * cleanliness_weight
        
        # Apply recency penalty from past_positions_grid
        if 0 <= new_y < self.cage.height and 0 <= new_x < self.cage.width:
            cell_value = self.past_positions_grid[new_y, new_x]
            if cell_value != -1:  # If it's been visited before
                recency_penalty = max(0, 1 - (cell_value / memory_decay))
                score -= recency_penalty
        
        # Ensure score is positive
        score = max(0.01, score)
        move_scores.append(score)
    
    # Normalize scores to probabilities
    total_score = sum(move_scores)
    move_probabilities = [score/total_score for score in move_scores]
    
    # Choose move based on calculated probabilities
    chosen_index = np.random.choice(len(possible_moves), p=move_probabilities)
    dx, dy = possible_moves[chosen_index]
    
    # Execute the move and update tracking as before
    new_x, new_y = self.x + dx, self.y + dy
    if self.cage and self.cage.is_valid_position(new_x, new_y):
        self.x, self.y = new_x, new_y
    
    # Update past positions grid
    if self.past_positions_grid is not None:
        self.past_positions_grid[self.past_positions_grid != -1] += 1
        self.past_positions_grid[self.y, self.x] = 0
    
    self.consume_energy()
