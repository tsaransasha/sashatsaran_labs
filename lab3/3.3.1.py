import math
import os


# Базовий клас
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
        # Перевірка: сторони мають бути додатними та виконуватися нерівність трикутника
        if a <= 0 or b <= 0 or c <= 0:
            raise ValueError("Сторони трикутника повинні бути додатними")
        if not (a + b > c and a + c > b and b + c > a):
            raise ValueError("Трикутник із такими сторонами не існує")
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
        if a <= 0 or b <= 0:
            raise ValueError("Сторони прямокутника повинні бути додатними")
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
        if a <= 0 or b <= 0 or c <= 0 or d <= 0:
            raise ValueError("Параметри трапеції повинні бути додатними")
        self.a, self.b, self.c, self.d = a, b, c, d

    def dimension(self):
        return 2

    def perimeter(self):
        return self.a + self.b + self.c + self.d

    def square(self):

        try:
            h = math.sqrt(max(0, self.c ** 2 - ((self.a - self.b) ** 2) / 4))
            return (self.a + self.b) / 2 * h
        except:
            return 0

    def volume(self):
        return self.square()


class Parallelogram(Figure):
    def __init__(self, a, b, h):
        if a <= 0 or b <= 0 or h <= 0:
            raise ValueError("Параметри паралелограма повинні бути додатними")
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
        if r <= 0:
            raise ValueError("Радіус має бути додатним")
        self.r = r

    def dimension(self):
        return 2

    def perimeter(self):
        return 2 * math.pi * self.r

    def square(self):
        return math.pi * self.r ** 2

    def volume(self):
        return self.square()


# 3D

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
        if h <= 0:
            raise ValueError("Висота має бути додатною")
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
        if c <= 0:
            raise ValueError("Висота (c) має бути додатною")
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
        # Створюємо правильний трикутник в основі (a, a, a)
        super().__init__(a, a, a)
        if h <= 0:
            raise ValueError("Висота піраміди має бути додатною")
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
        if h <= 0:
            raise ValueError("Висота піраміди має бути додатною")
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
        if h <= 0:
            raise ValueError("Висота призми має бути додатною")
        self.h = h

    def dimension(self):
        return 3

    def height(self):
        return self.h

    def squareBase(self):
        return super().square()

    def volume(self):
        return self.squareBase() * self.h


# Допоміжна функція

def create_figure(line):
    try:
        parts = line.split()
        if not parts:
            return None

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

    except (ValueError, TypeError, ZeroDivisionError):

        return None

    return None




def find_max_figure(filepath):
    figures = []

    if not os.path.exists(filepath):
        return None

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            fig = create_figure(line)
            if fig:
                figures.append(fig)

    if not figures:
        return None


    return max(figures, key=lambda f: f.volume())


# Головний блок

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, "input01.txt")

    # Створимо файл для тесту, якщо його немає
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write("Triangle 3 4 5\n")
            f.write("Rectangle 10 20\n")
            f.write("Circle 5\n")
            f.write("Triangle 1 1 10\n")  # Некоректний (не створиться)
            f.write("Ball 10\n")

    fig = find_max_figure(file_path)

    if fig:
        print(f"Найбільша фігура: {type(fig).__name__}")
        print(f"Міра (об'єм/площа): {fig.volume():.2f}")
    else:
        print("Немає коректних фігур у файлі.")
