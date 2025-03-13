from src.GridObject import GridObject

class Consumable(GridObject):
    def __init__(self, x, y, max_amount=10):
        super().__init__(x, y)
        self.max_amount = max_amount
        self.current_amount = max_amount
    
    def consume(self, amount=1):
        if self.current_amount >= amount:
            self.current_amount -= amount
            return 1
        return 0
    
    def fill(self, amount=None):
        if amount is None:
            self.current_amount = self.max_amount
        else:
            self.current_amount = min(self.current_amount + amount, self.max_amount)