from abc import ABC

class GridObject(ABC):
    def __init__(self, x, y):
        self.x = x
        self.y = y