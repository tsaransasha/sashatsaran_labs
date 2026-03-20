import math

# Базовий клас фігури
class Shape:
    def area(self):
        raise NotImplementedError("Method area() must be implemented")

    def perimeter(self):
        raise NotImplementedError("Method perimeter() must be implemented")


# --- Класи конкретних фігур ---
class Triangle(Shape):
    def __init__(self, a, b, c):
        if a <= 0 or b <= 0 or c <= 0:
            raise ValueError("Triangle sides must be positive")
        if a + b <= c or a + c <= b or b + c <= a:
            raise ValueError("Triangle with such sides does not exist")
        self.a = a
        self.b = b
        self.c = c

    def perimeter(self):
        return self.a + self.b + self.c

    def area(self):
        p = self.perimeter() / 2
        value = p * (p - self.a) * (p - self.b) * (p - self.c)
        if value < 0:
            raise ValueError("Cannot calculate triangle area")
        return math.sqrt(value)

    def __str__(self):
        return f"Triangle({self.a}, {self.b}, {self.c})"


class Rectangle(Shape):
    def __init__(self, a, b):
        if a <= 0 or b <= 0:
            raise ValueError("Rectangle sides must be positive")
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
        if a <= 0 or b <= 0 or c <= 0 or d <= 0:
            raise ValueError("Trapeze sides must be positive")
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        if not self._is_valid():
            raise ValueError("Trapeze with such sides does not exist")

    def _is_valid(self):
        diff = abs(self.a - self.b)
        summ = self.c + self.d
        return diff < summ

    def perimeter(self):
        return self.a + self.b + self.c + self.d

    def area(self):
        if self.a == self.b:
            raise ValueError("Cannot calculate trapeze area with equal bases")
        diff = abs(self.a - self.b)
        x = (diff ** 2 + self.c ** 2 - self.d ** 2) / (2 * diff)
        h_squared = self.c ** 2 - x ** 2
        if h_squared <= 0:
            raise ValueError("Cannot calculate trapeze area")
        h = math.sqrt(h_squared)
        return (self.a + self.b) * h / 2

    def __str__(self):
        return f"Trapeze({self.a}, {self.b}, {self.c}, {self.d})"


class Parallelogram(Shape):
    def __init__(self, a, b, h):
        if a <= 0 or b <= 0 or h <= 0:
            raise ValueError("Parallelogram sides and height must be positive")
        if h > a:
            raise ValueError("Height cannot be greater than the corresponding side")
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
        if r <= 0:
            raise ValueError("Circle radius must be positive")
        self.r = r

    def perimeter(self):
        return 2 * math.pi * self.r

    def area(self):
        return math.pi * self.r ** 2

    def __str__(self):
        return f"Circle({self.r})"


# --- Допоміжні функції ---
def parse_float_values(values):
    numbers = []
    for value in values:
        try:
            numbers.append(float(value))
        except ValueError:
            raise ValueError(f"'{value}' is not a number")
    return numbers


def create_shape(line):
    parts = line.split()
    if not parts:
        raise ValueError("Empty line")

    figure_name = parts[0]
    params = parts[1:]

    if figure_name == "Triangle":
        if len(params) != 3:
            raise ValueError("Triangle must have 3 parameters")
        a, b, c = parse_float_values(params)
        return Triangle(a, b, c)
    elif figure_name == "Rectangle":
        if len(params) != 2:
            raise ValueError("Rectangle must have 2 parameters")
        a, b = parse_float_values(params)
        return Rectangle(a, b)
    elif figure_name == "Trapeze":
        if len(params) != 4:
            raise ValueError("Trapeze must have 4 parameters")
        a, b, c, d = parse_float_values(params)
        return Trapeze(a, b, c, d)
    elif figure_name == "Parallelogram":
        if len(params) != 3:
            raise ValueError("Parallelogram must have 3 parameters")
        a, b, h = parse_float_values(params)
        return Parallelogram(a, b, h)
    elif figure_name == "Circle":
        if len(params) != 1:
            raise ValueError("Circle must have 1 parameter")
        r = parse_float_values(params)[0]
        return Circle(r)
    else:
        raise ValueError(f"Unknown figure: {figure_name}")


def read_shapes_from_file(filename):
    shapes = []
    with open(filename, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                shape = create_shape(line)
                shapes.append(shape)
            except ValueError as error:
                print(f"File {filename}, line {line_number}: {error}")
    return shapes


def find_shape_with_max_area(shapes):
    valid_shapes = []
    for shape in shapes:
        try:
            _ = shape.area()
            valid_shapes.append(shape)
        except ValueError:
            continue
    if not valid_shapes:
        return None
    return max(valid_shapes, key=lambda s: s.area())


def find_shape_with_max_perimeter(shapes):
    valid_shapes = []
    for shape in shapes:
        try:
            _ = shape.perimeter()
            valid_shapes.append(shape)
        except ValueError:
            continue
    if not valid_shapes:
        return None
    return max(valid_shapes, key=lambda s: s.perimeter())


def process_file(filename):
    print(f"\nProcessing file: {filename}")
    shapes = read_shapes_from_file(filename)

    if not shapes:
        print("No valid shapes found in file")
        return

    max_area_shape = find_shape_with_max_area(shapes)
    max_perimeter_shape = find_shape_with_max_perimeter(shapes)

    if max_area_shape:
        print("Shape with maximum area:")
        print(max_area_shape)
        print(f"Area = {max_area_shape.area():.2f}")
    else:
        print("No shape with valid area found")

    if max_perimeter_shape:
        print("Shape with maximum perimeter:")
        print(max_perimeter_shape)
        print(f"Perimeter = {max_perimeter_shape.perimeter():.2f}")
    else:
        print("No shape with valid perimeter found")


def main():
    files = ["input01.txt", "input02.txt", "input03.txt"]
    for filename in files:
        process_file(filename)


if __name__ == "__main__":
    main()