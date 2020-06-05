import math
from collections import namedtuple
from typing import List

Point = namedtuple("Point", ["x", "y"])


class Vector(object):
    def __init__(self, x: float, y: float):
        self._point = Point(x, y)

    @property
    def x(self) -> float:
        return self._point.x

    @x.setter
    def x(self, new_x: float):
        self._point = Point(new_x, self.y)

    @property
    def y(self) -> float:
        return self._point.y

    @y.setter
    def y(self, new_y: float):
        self._point = Point(self.x, new_y)

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other: "Vector") -> "Vector":
        pass

    def add(self, number: float):
        pass

    @staticmethod
    def sum(vectors: List["Vector"]) -> "Vector":
        x = sum([p.x for p in vectors])
        y = sum([p.y for p in vectors])
        return Vector(x, y)

    def multiply(self, number: float) -> "Vector":
        return Vector(self.x * number, self.y * number)

    def distance(self, other: "Vector") -> float:
        x = pow((self.x - other.x), 2)
        y = pow((self.y - other.y), 2)
        return math.sqrt(x + y)

    def magnitude(self):
        x = pow(self.x, 2)
        y = pow(self.y, 2)
        return math.sqrt(x + y)

    def dot(self, other: "Vector") -> float:
        # angle = self.angle_between(other)
        # return self.magnitude() * other.magnitude() * math.cos(angle)
        return (self.x * other.x) + (self.y * other.y)

    # def cross(self, other: "Vector"):
    #     pass

    def unit(self):
        pass

    def angle(self):
        pass

    def angle_between(self, other: "Vector"):
        pass

    def rotate(self, angle):
        pass

    def limit(self, upper=None, lower=None):
        pass
