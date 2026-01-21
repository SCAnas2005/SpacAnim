from math import sqrt

class vec2:
    def __init__(self, x:float, y:float) -> None:
        self.x = x
        self.y = y

    def __add__(self, other):
        if not isinstance(other, vec2):
            return NotImplemented
        return vec2(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        if (not isinstance(other, vec2)):
            return NotImplemented
        return vec2(self.x-other.x, self.y-other.y)

    def __radd__(self, other):
        return self + other

    def __mul__(self, other):
        if isinstance(other, vec2):
            return vec2(self.x*other.x, self.y*other.y)
        elif isinstance(other, (float, int)):
            return vec2(self.x*other, self.y*other)
        return NotImplemented

    def __rmul__(self, other):
        return self * other

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, vec2):
            return NotImplemented
        return self.x == value.x and self.y == value.y

    @classmethod
    def zero(cls):
        return vec2(0,0)
    

    def squared(self):
        return (self.x*self.x + self.y*self.y)

    def magnitude(self):
        return sqrt(self.squared())
    def normalize(self):
        length = self.magnitude()
        if (length == 0):
            return vec2(0,0)
        return vec2(self.x/length, self.y/length)

    def toTuple(self) -> tuple:
        return (self.x, self.y)
    
    def __str__(self) -> str:
        return f"({int(self.x)}, {int(self.y)})"
    

def clamp(n, min, max):
    if n < min:
        return min
    elif n > max:
        return max
    else:
        return n