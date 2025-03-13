from src.GridObject import GridObject
from src.Consumable import Consumable

class Food(Consumable):
    def __init__(self, x, y, max_amount=100):
        super().__init__(x, y, max_amount)
