from src.GridObject import GridObject
from src.Consumable import Consumable

class Water(Consumable):
    def __init__(self, x, y, max_amount=1000):
        super().__init__(x, y, max_amount)