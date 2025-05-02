import random
from src.GridObject import GridObject
from src.Cage import Cage
from abc import ABC
import numpy as np
import random


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






class WeightedRandomChicken(Chicken):
    def __init__(self, x, y, cage=None):
        super().__init__(x, y, cage)
        
        # Initialize grid that tracks how long ago she was in each place
        # Only initialize the grid if cage is provided, otherwise delay initialization
        self.past_positions_grid = None
        if self.cage is not None:
            self.initialize_grid()
        
        # Initialize coordinates for food, water, and bath
        self.food_coords = []
        self.water_coords = []
        self.bath_coords = []
        
        # Update resource coordinates if cage is provided
        self.update_resource_coordinates()
        
    def initialize_grid(self):
        """Initialize the past positions grid when cage is available."""
        if self.cage is not None:
            self.past_positions_grid = np.full((self.cage.height, self.cage.width), -1, dtype=int)
            # Set the current position to 0
            self.past_positions_grid[self.y, self.x] = 0
    
    def update_resource_coordinates(self):
        """Update coordinates for food, water, and bath sources."""
        if self.cage is not None:
            self.food_coords = [(food.x, food.y) for food in self.cage.food_sources]
            self.water_coords = [(water.x, water.y) for water in self.cage.water_sources]
            self.bath_coords = [(bath.x, bath.y) for bath in self.cage.bathing_areas]
    
    def set_cage(self, cage):
        """Method to set or update the cage reference."""
        self.cage = cage
        self.initialize_grid()
        self.update_resource_coordinates()

    def move(self):
        # Create grid if it doesn't exist yet (e.g., if cage was set after initialization)
        if self.past_positions_grid is None and self.cage is not None:
            self.initialize_grid()
            self.update_resource_coordinates()
        
        # Original move logic
        # Choose a random move (stand still is allowed)
        dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)])
        new_x, new_y = self.x + dx, self.y + dy
        
        # If the new position is valid, move there
        if self.cage and self.cage.is_valid_position(new_x, new_y):
            self.x, self.y = new_x, new_y

        # After moving, update past_positions_grid:
        if self.past_positions_grid is not None:
            # First, increment all cells that are not -1
            self.past_positions_grid[self.past_positions_grid != -1] += 1

            # Then, set the current position to 0
            self.past_positions_grid[self.y, self.x] = 0

        # Use up energy
        self.consume_energy()


class FollowerChicken(WeightedRandomChicken):
    def __init__(self, x, y, cage=None):
        super().__init__(x, y, cage)
        
        # Initialize lists for friends and enemies (these will hold references to other chicken objects)
        self.friends = []
        self.enemies = []
        
        # Parameters for social behavior
        self.friend_attraction = 2.5   # How strongly the chicken is attracted to friends
        self.enemy_repulsion = 3.0     # How strongly the chicken avoids enemies
        self.social_distance_factor = 5.0  # How quickly social effects drop off with distance
    
    def add_friend(self, chicken):
        """Add a chicken to the friends list."""
        if chicken not in self.friends:
            self.friends.append(chicken)
    
    def add_enemy(self, chicken):
        """Add a chicken to the enemies list."""
        if chicken not in self.enemies:
            self.enemies.append(chicken)
    
    def remove_friend(self, chicken):
        """Remove a chicken from the friends list."""
        if chicken in self.friends:
            self.friends.remove(chicken)
    
    def remove_enemy(self, chicken):
        """Remove a chicken from the enemies list."""
        if chicken in self.enemies:
            self.enemies.remove(chicken)
            
    def move(self):
        possible_moves = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]  # Including stay still
        move_scores = []
        
        # Parameters
        memory_decay = 10  # How quickly chicken "forgets" visited locations
        base_random_weight = 1.0  # Base weight for randomness
        
        # Calculate need levels (higher value = greater need)
        # Fix: Use self.food instead of self.hunger
        hunger_need = max(0, (100 - self.food) / 100)  # 0 when full, 1 when starving
        # Fix: Use self.water instead of self.thirst
        thirst_need = max(0, (100 - self.water) / 100)  # 0 when not thirsty, 1 when very thirsty
        # Fix: Use self.clean instead of self.cleanliness
        cleanliness_need = max(0, (100 - self.clean) / 100)  # 0 when clean, 1 when dirty
        
        # Need weights - how much each need influences decisions
        hunger_weight = 20
        thirst_weight = 3.5  
        cleanliness_weight = 1.0  # Less critical than food/water
        
        # Calculate current distances to nearest resources
        current_dist_to_food = min([abs(self.x - fx) + abs(self.y - fy) for fx, fy in self.food_coords], default=float('inf'))
        current_dist_to_water = min([abs(self.x - wx) + abs(self.y - wy) for wx, wy in self.water_coords], default=float('inf'))
        current_dist_to_bath = min([abs(self.x - bx) + abs(self.y - by) for bx, by in self.bath_coords], default=float('inf'))
        
        # Calculate scores for each possible move
        for dx, dy in possible_moves:
            new_x, new_y = self.x + dx, self.y + dy
            
            # Skip invalid moves
            if not self.cage or not self.cage.is_valid_position(new_x, new_y):
                move_scores.append(0)
                continue
            
            # Start with base random score
            score = base_random_weight
            
            # Calculate new distances after potential move
            new_pos = (new_x, new_y)
            
            # Direct resource bonus - highest if standing on the resource
            if new_pos in self.food_coords:
                score += hunger_need * hunger_weight * 3  # Extra bonus for being on food
            
            if new_pos in self.water_coords:
                score += thirst_need * thirst_weight * 3  # Extra bonus for being on water
            
            if new_pos in self.bath_coords:
                score += cleanliness_need * cleanliness_weight * 3  # Extra bonus for being on bath
            
            # Distance-based attraction to resources
            new_dist_to_food = min([abs(new_x - fx) + abs(new_y - fy) for fx, fy in self.food_coords], default=float('inf'))
            if new_dist_to_food < current_dist_to_food:
                # Bonus for moving closer to food, scaled by hunger need
                score += hunger_need * hunger_weight * (current_dist_to_food - new_dist_to_food) / max(1, current_dist_to_food)
            
            new_dist_to_water = min([abs(new_x - wx) + abs(new_y - wy) for wx, wy in self.water_coords], default=float('inf'))
            if new_dist_to_water < current_dist_to_water:
                # Bonus for moving closer to water, scaled by thirst need
                score += thirst_need * thirst_weight * (current_dist_to_water - new_dist_to_water) / max(1, current_dist_to_water)
            
            new_dist_to_bath = min([abs(new_x - bx) + abs(new_y - by) for bx, by in self.bath_coords], default=float('inf'))
            if new_dist_to_bath < current_dist_to_bath:
                # Bonus for moving closer to bath, scaled by cleanliness need
                score += cleanliness_need * cleanliness_weight * (current_dist_to_bath - new_dist_to_bath) / max(1, current_dist_to_bath)
            
            # Social interaction calculations - the key addition for FollowerChicken
            
            # Friend attraction - prefer squares closer to friends
            for friend in self.friends:
                current_dist_to_friend = abs(self.x - friend.x) + abs(self.y - friend.y)
                new_dist_to_friend = abs(new_x - friend.x) + abs(new_y - friend.y)
                
                # Calculate social attraction score
                # Higher when new position is closer to friend
                # Inversely proportional to distance (closer friends have more influence)
                if new_dist_to_friend < current_dist_to_friend:
                    # Moving closer to friend - positive score
                    proximity_factor = 1 / max(1, new_dist_to_friend)
                    score += self.friend_attraction * proximity_factor
                elif new_dist_to_friend > 0:
                    # Still apply some attraction to be near friend, even if not moving closer
                    proximity_factor = 1 / max(1, new_dist_to_friend)
                    score += self.friend_attraction * proximity_factor * 0.5  # Reduced effect
            
            # Enemy repulsion - avoid squares closer to enemies
            for enemy in self.enemies:
                current_dist_to_enemy = abs(self.x - enemy.x) + abs(self.y - enemy.y)
                new_dist_to_enemy = abs(new_x - enemy.x) + abs(new_y - enemy.y)
                
                # Calculate social repulsion score
                # Higher when new position increases distance from enemy
                if new_dist_to_enemy > current_dist_to_enemy:
                    # Moving away from enemy - positive score
                    distance_increase = new_dist_to_enemy - current_dist_to_enemy
                    score += self.enemy_repulsion * (distance_increase / self.social_distance_factor)
                elif new_dist_to_enemy < current_dist_to_enemy:
                    # Moving toward enemy - negative score (penalty)
                    distance_decrease = current_dist_to_enemy - new_dist_to_enemy
                    score -= self.enemy_repulsion * (distance_decrease / self.social_distance_factor)
                    
                # Additional penalty for being very close to enemy
                if new_dist_to_enemy <= 2:  # If would end up within 2 squares of enemy
                    proximity_penalty = self.enemy_repulsion * (1 / max(1, new_dist_to_enemy))
                    score -= proximity_penalty * 2  # Double penalty for close proximity
            
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