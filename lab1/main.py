import math
import os


class Triangle:
    def __init__(self, a, b, c):
        self.a, self.b, self.c = float(a), float(b), float(c)
        self.name = "Triangle"
        # Перевірка існування через assert
        assert self.a > 0 and self.b > 0 and self.c > 0, "Sides must be positive"
        assert (self.a + self.b > self.c and
                self.a + self.c > self.b and
                self.b + self.c > self.a), "Triangle inequality violation"

    def perim(self):
        return self.a + self.b + self.c

    def area(self):
        p = self.perim() / 2
        return math.sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))


class Rectangle:
    def __init__(self, a, b):
        self.a, self.b = float(a), float(b)
        self.name = "Rectangle"
        assert self.a > 0 and self.b > 0, "Sides must be positive"

    def perim(self):
        return 2 * (self.a + self.b)

    def area(self):
        return self.a * self.b


class Trapeze:
    def __init__(self, a, b, c, d):
        self.a, self.b, self.c, self.d = float(a), float(b), float(c), float(d)
        self.name = "Trapeze"
        diff = abs(self.a - self.b)
        assert all(x > 0 for x in [self.a, self.b, self.c, self.d]), "Sides must be positive"
        assert diff != 0, "Bases cannot be equal (not a trapeze)"
        assert diff < (self.c + self.d) and diff > abs(self.c - self.d), "Trapeze cannot exist"

    def perim(self):
        return self.a + self.b + self.c + self.d

    def area(self):
        diff = abs(self.a - self.b)
        s = (self.a + self.b) / 2
        h_part = ((-diff + self.c + self.d) * (diff + self.c - self.d) * (diff - self.c + self.d) * (
                    diff + self.c + self.d))
        h = (1 / (2 * diff)) * math.sqrt(h_part)
        return s * h


class Parallelogram:
    def __init__(self, a, b, h):
        self.a, self.b, self.h = float(a), float(b), float(h)
        self.name = "Parallelogram"
        assert self.a > 0 and self.b > 0 and self.h > 0, "Parameters must be positive"
        assert self.h <= self.b, "Height cannot be greater than side b"

    def perim(self):
        return 2 * (self.a + self.b)

    def area(self):
        return self.a * self.h


class Circle:
    def __init__(self, r):
        self.r = float(r)
        self.name = "Circle"
        assert self.r > 0, "Radius must be positive"

    def perim(self):
        return 2 * math.pi * self.r

    def area(self):
        return math.pi * self.r ** 2


def create_figure(line):
    parts = line.strip().split()
    if not parts:
        return None

    figure_type = parts[0]
    params = parts[1:]

    try:

        if figure_type == "Triangle" and len(params) == 3:
            return Triangle(*params)
        elif figure_type == "Rectangle" and len(params) == 2:
            return Rectangle(*params)
        elif figure_type == "Trapeze" and len(params) == 4:
            return Trapeze(*params)
        elif figure_type == "Parallelogram" and len(params) == 3:
            return Parallelogram(*params)
        elif figure_type == "Circle" and len(params) == 1:
            return Circle(*params)
    except (ValueError, AssertionError, ZeroDivisionError):
        return None

    return None


def analyze(filename):
    figures = []
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, filename)

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                fig = create_figure(line)
                if fig is not None:
                    figures.append(fig)
    except FileNotFoundError:
        print(f"Файл {filename} не знайдено.")
        return

    if not figures:
        print(f"У файлі {filename} не знайдено коректних даних.")
        return

    max_area_figure = max(figures, key=lambda x: x.area())
    max_perim_figure = max(figures, key=lambda x: x.perim())

    print(f"Файл: {filename}")
    print(f"Найбільша площа: {max_area_figure.name}, {max_area_figure.area():.2f}")
    print(f"Найбільший периметр: {max_perim_figure.name}, {max_perim_figure.perim():.2f}")
    print()


files = ["input01.txt", "input02.txt", "input03.txt"]

for filename in files:
    analyze(filename)