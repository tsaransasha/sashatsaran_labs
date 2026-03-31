import turtle
import random

# Налаштування вікна

screen = turtle.Screen()
screen.setup(1200, 800)
screen.bgcolor("lightyellow")
screen.title("Букет квітів - ООП Turtle")

t = turtle.Turtle()
t.speed(0)
t.hideturtle()
t.pensize(2)


# Клас Petal (Пелюстка)

class Petal:
    def __init__(self, color, size):
        self.color = color
        self.size = size

    def draw(self, turtle_obj, x, y, angle):
        turtle_obj.penup()
        turtle_obj.goto(x, y)
        turtle_obj.setheading(angle)
        turtle_obj.pendown()

        turtle_obj.fillcolor(self.color)
        turtle_obj.begin_fill()

        turtle_obj.circle(self.size, 60)
        turtle_obj.left(120)
        turtle_obj.circle(self.size, 60)

        turtle_obj.end_fill()


# Клас Leaf (Листок)

class Leaf:
    def __init__(self, color="green", size=30, angle=45):
        self.color = color
        self.size = size
        self.angle = angle

    def draw(self, turtle_obj, x, y, stem_angle):
        turtle_obj.penup()
        turtle_obj.goto(x, y)
        turtle_obj.setheading(stem_angle + self.angle)
        turtle_obj.pendown()

        turtle_obj.fillcolor(self.color)
        turtle_obj.begin_fill()

        turtle_obj.circle(self.size, 60)
        turtle_obj.left(120)
        turtle_obj.circle(self.size, 60)

        turtle_obj.end_fill()


# Клас Stem (Стебло)

class Stem:
    def __init__(self, length=150, color="forestgreen", angle=90):
        self.length = length
        self.color = color
        self.angle = angle

    def draw(self, turtle_obj, x, y):
        turtle_obj.penup()
        turtle_obj.goto(x, y)
        turtle_obj.setheading(self.angle)
        turtle_obj.pendown()

        turtle_obj.pencolor(self.color)
        turtle_obj.pensize(4)
        turtle_obj.forward(self.length)

        top_x = turtle_obj.xcor()
        top_y = turtle_obj.ycor()

        return top_x, top_y


# Клас Flower (Квітка)

class Flower:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.flower_color = random.choice([
            "red", "pink", "yellow", "orange",
            "violet", "purple", "blue", "white"
        ])

        self.stem = Stem(
            length=random.randint(130, 190),
            color=random.choice(["green", "forestgreen", "darkgreen", "seagreen"]),
            angle=random.randint(85, 95)  # менший нахил
        )

        self.center_color = random.choice(["gold", "orange", "yellow", "brown"])
        self.center_size = random.randint(10, 15)

        self.petal_count = random.randint(6, 10)
        self.petal_size = random.randint(18, 28)  # менші пелюстки

        self.petals = []
        for _ in range(self.petal_count):
            self.petals.append(Petal(self.flower_color, self.petal_size))

        self.leaves = [
            Leaf(
                color=random.choice(["green", "limegreen", "forestgreen", "seagreen"]),
                size=random.randint(20, 30),
                angle=random.choice([-50, 50])
            ),
            Leaf(
                color=random.choice(["green", "limegreen", "forestgreen", "seagreen"]),
                size=random.randint(20, 30),
                angle=random.choice([-40, 40])
            )
        ]

    def draw_center(self, turtle_obj, x, y):
        turtle_obj.penup()
        turtle_obj.goto(x, y - self.center_size)
        turtle_obj.setheading(0)
        turtle_obj.pendown()

        turtle_obj.pencolor("black")
        turtle_obj.fillcolor(self.center_color)
        turtle_obj.begin_fill()
        turtle_obj.circle(self.center_size)
        turtle_obj.end_fill()

    def draw(self, turtle_obj):
        top_x, top_y = self.stem.draw(turtle_obj, self.x, self.y)

        leaf1_y = self.y + self.stem.length * 0.35
        leaf2_y = self.y + self.stem.length * 0.6

        self.leaves[0].draw(turtle_obj, self.x, leaf1_y, self.stem.angle)
        self.leaves[1].draw(turtle_obj, self.x, leaf2_y, self.stem.angle)

        for i, petal in enumerate(self.petals):
            angle = i * (360 / self.petal_count)
            petal.draw(turtle_obj, top_x, top_y, angle)

        self.draw_center(turtle_obj, top_x, top_y)


# Букет із 6 квіток

bouquet_positions = [
    (-350, -250),
    (-210, -220),
    (-70, -250),
    (70, -220),
    (210, -250),
    (350, -220)
]

flowers = []

for pos in bouquet_positions:
    flower = Flower(pos[0], pos[1])
    flowers.append(flower)

for flower in flowers:
    flower.draw(t)

turtle.done()
