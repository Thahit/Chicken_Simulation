from src.GridObject import GridObject
from src.Consumable import Consumable

class Water(Consumable):
    def __init__(self, x, y, max_amount=10000):
        super().__init__(x, y, max_amount)

    def consume(self, amount=50):
        return super().consume(amount)