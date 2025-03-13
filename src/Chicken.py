import random
from src.GridObject import GridObject
from src.Cage import Cage
from abc import ABC


class Chicken(GridObject, ABC):
    _id_counter = 0
    def __init__(self, x, y, cage=None):
        super().__init__(x, y)
        self.cage = cage
        self.food = 100
        self.water = 100
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
        


class RandomChicken(Chicken):
    def move(self):
        dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)])  # Allow standing still
        new_x, new_y = self.x + dx, self.y + dy
        
        if self.cage and self.cage.is_valid_position(new_x, new_y):
            self.x, self.y = new_x, new_y