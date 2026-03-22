import math
import os


class Triangle:
    def __init__(self, a, b, c):
        self.a = float(a)
        self.b = float(b)
        self.c = float(c)
        self.name = "Triangle"

    def perim(self):
        if self.a + self.b <= self.c or self.a + self.c <= self.b or self.b + self.c <= self.a:
            return 0
        return self.a + self.b + self.c

    def area(self):
        if self.perim() == 0:
            return 0
        p = self.perim() / 2
        return math.sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))


class Rectangle:
    def __init__(self, a, b):
        self.a = float(a)
        self.b = float(b)
        self.name = "Rectangle"

    def perim(self):
        return 2 * (self.a + self.b)

    def area(self):
        return self.a * self.b


class Trapeze:
    def __init__(self, a, b, c, d):
        self.a = float(a)
        self.b = float(b)
        self.c = float(c)
        self.d = float(d)
        self.name = "Trapeze"

    def perim(self):
        return self.a + self.b + self.c + self.d

    def area(self):
        diff = abs(self.a - self.b)
        if diff == 0:
            return 0

        x = (diff ** 2 + self.c ** 2 - self.d ** 2) / (2 * diff)
        h2 = self.c ** 2 - x ** 2

        if h2 < 0:
            return 0

        h = math.sqrt(h2)
        return ((self.a + self.b) / 2) * h


class Parallelogram:
    def __init__(self, a, b, h):
        self.a = float(a)
        self.b = float(b)
        self.h = float(h)
        self.name = "Parallelogram"

    def perim(self):
        return 2 * (self.a + self.b)

    def area(self):
        return self.a * self.h


class Circle:
    def __init__(self, r):
        self.r = float(r)
        self.name = "Circle"

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
    except ValueError:
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
        print(f"У файлі {filename} не знайдено коректних даних для створення фігур.")
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