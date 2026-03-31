import math
import os


# ================== БАЗОВИЙ КЛАС ==================
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


# ================== 2D ФІГУРИ ==================

class Triangle(Figure):
    def __init__(self, a, b, c):
        self.a, self.b, self.c = a, b, c

    def dimension(self):
        return 2

    def perimeter(self):
        return self.a + self.b + self.c

    def square(self):
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
        # припущення: рівнобічна трапеція
        h = math.sqrt(self.c ** 2 - ((self.a - self.b) ** 2) / 4)
        return (self.a + self.b) / 2 * h

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


# ================== 3D ФІГУРИ ==================

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


# ================== СТВОРЕННЯ ФІГУРИ ==================

def create_figure(line):
    parts = line.split()
    name = parts[0]
    nums = list(map(float, parts[1:]))

    if name == "Triangle":
        return Triangle(*nums)
    elif name == "Rectangle":
        return Rectangle(*nums)
    elif name == "Trapeze":
        return Trapeze(*nums)
    elif name == "Parallelogram":
        return Parallelogram(*nums)
    elif name == "Circle":
        return Circle(*nums)
    elif name == "Ball":
        return Ball(*nums)
    elif name == "Cone":
        return Cone(*nums)
    elif name == "RectangularParallelepiped":
        return RectangularParallelepiped(*nums)
    elif name == "TriangularPyramid":
        return TriangularPyramid(*nums)
    elif name == "QuadrangularPyramid":
        return QuadrangularPyramid(*nums)
    elif name == "TriangularPrism":
        return TriangularPrism(*nums)

    return None


# ================== ПОШУК НАЙБІЛЬШОЇ ==================

def find_max_figure(filename):
    figures = []

    with open(filename) as f:
        for line in f:
            if not line.strip():
                continue
            fig = create_figure(line.strip())
            if fig:
                figures.append(fig)

    if not figures:
        return None

    return max(figures, key=lambda f: f.volume())


# ================== ГОЛОВНА ЧАСТИНА ==================

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, "input01.txt")

    fig = find_max_figure(file_path)

    if fig:
        print("Найбільша фігура:", type(fig).__name__)
        print("Міра:", fig.volume())
    else:
        print("Фігури не знайдені")
