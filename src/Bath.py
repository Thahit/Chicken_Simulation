from src.GridObject import GridObject
from src.Consumable import Consumable
import random

class Bath(Consumable):
    def __init__(self, x, y,):
        super().__init__(x, y, max_amount=-1)
    
    def consume(self):
        return random.randint(10, 25)
