from src.GridObject import GridObject
from src.Consumable import Consumable

class Food(Consumable):
    def __init__(self, x, y, max_amount=1000):
        super().__init__(x, y, max_amount)

    def consume(self, amount=25):
        super.consume(amount)