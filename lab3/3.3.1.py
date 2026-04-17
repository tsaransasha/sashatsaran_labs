import math
import os


# Base class
class Figure:
    def dimension(self):
        raise NotImplementedError()

    def perimeter(self):
        return None

    def square(self):
        return None

    def squareSurface(self):
        return None

    def squareBase(self):
        return None

    def height(self):
        return None

    def volume(self):
        raise NotImplementedError()


# 2D

class Triangle(Figure):
    def __init__(self, a, b, c):
        self.a, self.b, self.c = a, b, c

    def is_valid(self):
        return (self.a + self.b > self.c and
                self.a + self.c > self.b and
                self.b + self.c > self.a)

    def dimension(self):
        return 2

    def perimeter(self):
        return self.a + self.b + self.c if self.is_valid() else None

    def square(self):
        if not self.is_valid():
            return 0
        p = self.perimeter() / 2
        return math.sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))

    def volume(self):
        return self.square()


class Rectangle(Figure):
    def __init__(self, a, b):
        self.a, self.b = a, b

    def dimension(self):
        return 2

    def perimeter(self):
        return 2 * (self.a + self.b)

    def square(self):
        return self.a * self.b

    def volume(self):
        return self.square()


class Trapeze(Figure):
    def __init__(self, a, b, c, d):
        self.a, self.b, self.c, self.d = a, b, c, d

    def dimension(self):
        return 2

    def perimeter(self):
        return self.a + self.b + self.c + self.d

    def square(self):
        try:
            h = math.sqrt(self.c ** 2 - ((self.a - self.b) ** 2) / 4)
            return (self.a + self.b) / 2 * h
        except:
            return 0

    def volume(self):
        return self.square()


class Parallelogram(Figure):
    def __init__(self, a, b, h):
        self.a, self.b, self.h = a, b, h

    def dimension(self):
        return 2

    def perimeter(self):
        return 2 * (self.a + self.b)

    def square(self):
        return self.a * self.h

    def volume(self):
        return self.square()


class Circle(Figure):
    def __init__(self, r):
        self.r = r

    def dimension(self):
        return 2

    def perimeter(self):
        return 2 * math.pi * self.r

    def square(self):
        return math.pi * self.r ** 2

    def volume(self):
        return self.square()


#  3D

class Ball(Circle):
    def dimension(self):
        return 3

    def squareSurface(self):
        return 4 * math.pi * self.r ** 2

    def volume(self):
        return (4 / 3) * math.pi * self.r ** 3


class Cone(Circle):
    def __init__(self, r, h):
        super().__init__(r)
        self.h = h

    def dimension(self):
        return 3

    def height(self):
        return self.h

    def squareSurface(self):
        l = math.sqrt(self.r ** 2 + self.h ** 2)
        return math.pi * self.r * l

    def squareBase(self):
        return math.pi * self.r ** 2

    def volume(self):
        return (1 / 3) * math.pi * self.r ** 2 * self.h


class RectangularParallelepiped(Rectangle):
    def __init__(self, a, b, c):
        super().__init__(a, b)
        self.c = c

    def dimension(self):
        return 3

    def height(self):
        return self.c

    def squareSurface(self):
        return 2 * (self.a * self.b + self.a * self.c + self.b * self.c)

    def squareBase(self):
        return self.a * self.b

    def volume(self):
        return self.a * self.b * self.c


class TriangularPyramid(Triangle):
    def __init__(self, a, h):
        super().__init__(a, a, a)
        self.h = h

    def dimension(self):
        return 3

    def height(self):
        return self.h

    def squareBase(self):
        return super().square()

    def volume(self):
        return self.squareBase() * self.h / 3


class QuadrangularPyramid(Rectangle):
    def __init__(self, a, b, h):
        super().__init__(a, b)
        self.h = h

    def dimension(self):
        return 3

    def height(self):
        return self.h

    def squareBase(self):
        return self.a * self.b

    def volume(self):
        return self.squareBase() * self.h / 3


class TriangularPrism(Triangle):
    def __init__(self, a, b, c, h):
        super().__init__(a, b, c)
        self.h = h

    def dimension(self):
        return 3

    def height(self):
        return self.h

    def squareBase(self):
        return super().square()

    def volume(self):
        return self.squareBase() * self.h


# Create

def create_figure(line):
    try:
        parts = line.split()
        name = parts[0]
        nums = list(map(float, parts[1:]))

        mapping = {
            "Triangle": Triangle,
            "Rectangle": Rectangle,
            "Trapeze": Trapeze,
            "Parallelogram": Parallelogram,
            "Circle": Circle,
            "Ball": Ball,
            "Cone": Cone,
            "RectangularParallelepiped": RectangularParallelepiped,
            "TriangularPyramid": TriangularPyramid,
            "QuadrangularPyramid": QuadrangularPyramid,
            "TriangularPrism": TriangularPrism,
        }

        if name in mapping:
            return mapping[name](*nums)

    except:
        return None

    return None


# Search

def find_max_figure(filepath):
    figures = []

    with open(filepath) as f:
        for line in f:
            if not line.strip():
                continue

            fig = create_figure(line.strip())

            if fig:
                try:
                    val = fig.volume()
                    if val is not None:
                        figures.append(fig)
                except:
                    pass

    if not figures:
        return None

    return max(figures, key=lambda f: f.volume())


# Main

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, "input01.txt")

    fig = find_max_figure(file_path)

    if fig:
        print("Найбільша фігура:", type(fig).__name__)
        print("Міра:", fig.volume())
    else:
        print("Немає коректних фігур")
