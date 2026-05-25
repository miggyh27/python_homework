# Task 5

from __future__ import annotations

import math
from typing import Any


class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __str__(self) -> str:
        return f"Point({self.x}, {self.y})"

    def distance_to(self, other: Point) -> float:
        if not isinstance(other, Point):
            raise TypeError("distance_to expects a Point")
        return math.hypot(other.x - self.x, other.y - self.y)


class Vector(Point):
    def __str__(self) -> str:
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other: Any) -> Vector:
        if not isinstance(other, Point):
            return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)

    def __radd__(self, other: Any) -> Vector:
        if not isinstance(other, Point):
            return NotImplemented
        return Vector(other.x + self.x, other.y + self.y)


if __name__ == "__main__":
    p = Point(3, 4)
    q = Point(0, 0)
    r = Point(3, 4)
    print(p, q, "p == q?", p == q, "p == r?", p == r)
    print("distance p to q:", p.distance_to(q))

    v1 = Vector(1, 2)
    v2 = Vector(4, 6)
    print(v1, v2)
    summed = v1 + v2
    print("v1 + v2 =", summed)
    print("type of sum:", type(summed).__name__)
    print("Point + Vector:", Point(1, 1) + Vector(2, 3))
