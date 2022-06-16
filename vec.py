# Custom vector class

class vec:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def list(self):
        return [self.x, self.y]

    def __add__(self, other):
        return vec(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        return vec(self.x * other, self.y * other)

    def __imul__(self, other):
        return vec(self.x * other, self.y * other)
