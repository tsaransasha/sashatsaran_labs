import math


class Shape:
    def area(self):
        raise NotImplementedError

    def perimeter(self):
        raise NotImplementedError


class Triangle(Shape):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def perimeter(self):
        return self.a + self.b + self.c

    def area(self):
        p = self.perimeter() / 2
        return math.sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))

    def __str__(self):
        return f"Triangle({self.a}, {self.b}, {self.c})"


class Rectangle(Shape):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def perimeter(self):
        return 2 * (self.a + self.b)

    def area(self):
        return self.a * self.b

    def __str__(self):
        return f"Rectangle({self.a}, {self.b})"


class Trapeze(Shape):
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def perimeter(self):
        return self.a + self.b + self.c + self.d

    def area(self):
        diff = abs(self.a - self.b)

        if diff == 0:
            return 0

        x = (diff ** 2 + self.c ** 2 - self.d ** 2) / (2 * diff)
        h_squared = self.c ** 2 - x ** 2

        if h_squared < 0:
            return 0

        h = math.sqrt(h_squared)
        return (self.a + self.b) * h / 2

    def __str__(self):
        return f"Trapeze({self.a}, {self.b}, {self.c}, {self.d})"


class Parallelogram(Shape):
    def __init__(self, a, b, h):
        self.a = a
        self.b = b
        self.h = h

    def perimeter(self):
        return 2 * (self.a + self.b)

    def area(self):
        return self.a * self.h

    def __str__(self):
        return f"Parallelogram({self.a}, {self.b}, {self.h})"


class Circle(Shape):
    def __init__(self, r):
        self.r = r

    def perimeter(self):
        return 2 * math.pi * self.r

    def area(self):
        return math.pi * self.r ** 2

    def __str__(self):
        return f"Circle({self.r})"


def create_shape(line):
    parts = line.split()
    figure_name = parts[0]

    if figure_name == "Triangle":
        a, b, c = map(float, parts[1:4])
        return Triangle(a, b, c)

    if figure_name == "Rectangle":
        a, b = map(float, parts[1:3])
        return Rectangle(a, b)

    if figure_name == "Trapeze":
        a, b, c, d = map(float, parts[1:5])
        return Trapeze(a, b, c, d)

    if figure_name == "Parallelogram":
        a, b, h = map(float, parts[1:4])
        return Parallelogram(a, b, h)

    if figure_name == "Circle":
        r = float(parts[1])
        return Circle(r)

    raise ValueError(f"Unknown figure: {figure_name}")


def read_shapes_from_file(filename):
    shapes = []

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                shape = create_shape(line)
                shapes.append(shape)

    return shapes


def find_shape_with_max_area(shapes):
    return max(shapes, key=lambda shape: shape.area())


def find_shape_with_max_perimeter(shapes):
    return max(shapes, key=lambda shape: shape.perimeter())


def process_file(filename):
    print(f"Processing file: {filename}")

    shapes = read_shapes_from_file(filename)

    max_area_shape = find_shape_with_max_area(shapes)
    max_perimeter_shape = find_shape_with_max_perimeter(shapes)

    print("Shape with maximum area:")
    print(max_area_shape)
    print(f"Area = {max_area_shape.area():.2f}")

    print("Shape with maximum perimeter:")
    print(max_perimeter_shape)
    print(f"Perimeter = {max_perimeter_shape.perimeter():.2f}")

    print("-" * 40)


def main():
    files = ["input01.txt", "input02.txt", "input03.txt"]

    for filename in files:
        try:
            process_file(filename)
        except FileNotFoundError:
            print(f"File {filename} not found.")
            print("-" * 40)
        except Exception as error:
            print(f"Error while processing {filename}: {error}")
            print("-" * 40)


if __name__ == "__main__":
    main()
