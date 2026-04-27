import turtle


# бaзовий клас

class Figure:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.visible = False
        self.turtle = turtle.Turtle()
        self.turtle.speed(0)
        self.turtle.hideturtle()
        self.turtle.penup()

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def draw(self, color):
        pass

    def show(self):
        self.draw("black")
        self.visible = True

    def hide(self):
        self.draw("white")
        self.visible = False


#  Клас для хрестика

class Cross(Figure):

    def __init__(self, size=60):
        super().__init__()
        self.size = size

    def draw(self, color):
        self.turtle.penup()
        self.turtle.color(color)
        self.turtle.pensize(4)

        offset = self.size // 2

        # Перша діагональ (\)
        self.turtle.goto(self.x - offset, self.y + offset)
        self.turtle.pendown()
        self.turtle.goto(self.x + offset, self.y - offset)
        self.turtle.penup()

        # Друга діагональ (/)
        self.turtle.goto(self.x + offset, self.y + offset)
        self.turtle.pendown()
        self.turtle.goto(self.x - offset, self.y - offset)
        self.turtle.penup()


# Клас для нулика

class Circle(Figure):
    # зобразити

    def __init__(self, radius=25):
        super().__init__()
        self.radius = radius

    def draw(self, color):
        # малюємо
        self.turtle.penup()
        self.turtle.color(color)
        self.turtle.pensize(4)
        self.turtle.goto(self.x, self.y - self.radius)
        self.turtle.pendown()
        self.turtle.circle(self.radius)
        self.turtle.penup()


# ігрове поле

class GameBoard(Figure):

    def __init__(self, cell_size=100):
        super().__init__()
        self.cell_size = cell_size

    def draw(self, color):
        self.turtle.penup()
        self.turtle.color(color)
        self.turtle.pensize(2)

        size = self.cell_size * 3
        half = size // 2
        for i in range(1, 3):
            x = self.x - half + i * self.cell_size
            self.turtle.goto(x, self.y + half)
            self.turtle.pendown()
            self.turtle.goto(x, self.y - half)
            self.turtle.penup()

        for i in range(1, 3):
            y = self.y + half - i * self.cell_size
            self.turtle.goto(self.x - half, y)
            self.turtle.pendown()
            self.turtle.goto(self.x + half, y)
            self.turtle.penup()

    def get_cell_center(self, row, col):
        half = (self.cell_size * 3) // 2
        x = self.x - half + col * self.cell_size + self.cell_size // 2
        y = self.y + half - row * self.cell_size - self.cell_size // 2
        return x, y

    def get_cell_from_coords(self, px, py):
        half = (self.cell_size * 3) // 2

        col = int((px - self.x + half) // self.cell_size)
        row = int((self.y + half - py) // self.cell_size)

        if 0 <= row < 3 and 0 <= col < 3:
            return row, col
        return None


#  Клас гри

class TicTacToe:

    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("Хрестики-нулики")
        self.screen.setup(400, 450)
        self.screen.tracer(0)

        self.board = GameBoard(cell_size=100)
        self.board.setPosition(0, -25)
        self.board.show()

        self.cells = [[None for _ in range(3)] for _ in range(3)]
        self.figures = []
        self.current_player = "X"
        self.game_over = False

        self.status_turtle = turtle.Turtle()
        self.status_turtle.hideturtle()
        self.status_turtle.penup()
        self.status_turtle.goto(0, 170)
        self.update_status()

        self.screen.update()

        self.screen.onclick(self.on_click)
        self.screen.listen()

    def update_status(self):
        self.status_turtle.clear()
        if self.game_over:
            return
        text = f"Хід гравця: {self.current_player}"
        self.status_turtle.write(text, align="center", font=("Arial", 16, "bold"))

    def show_winner(self, winner):
        self.status_turtle.clear()
        if winner == "Нічия":
            text = "Нічия!"
        else:
            text = f"Переміг {winner}!"
        self.status_turtle.write(text, align="center", font=("Arial", 18, "bold"))

    def check_winner(self):

        lines = [
            # Рядки
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            # Стовпці
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            # Діагоналі
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)],
        ]

        for line in lines:
            values = [self.cells[r][c] for r, c in line]
            if values[0] and values[0] == values[1] == values[2]:
                return values[0]

        # Перевірка на нічию
        if all(self.cells[r][c] for r in range(3) for c in range(3)):
            return "Нічия"

        return None

    def on_click(self, px, py):
        if self.game_over:
            return

        cell = self.board.get_cell_from_coords(px, py)
        if cell is None:
            return

        row, col = cell

        if self.cells[row][col] is not None:
            return

        cx, cy = self.board.get_cell_center(row, col)

        if self.current_player == "X":
            figure = Cross(size=60)
        else:
            figure = Circle(radius=30)

        figure.setPosition(cx, cy)
        figure.show()
        self.figures.append(figure)

        self.cells[row][col] = self.current_player
        self.screen.update()

        # Перевірка переможця
        winner = self.check_winner()
        if winner:
            self.game_over = True
            self.show_winner(winner)
            self.screen.update()
            return

        # Зміна гравця
        self.current_player = "O" if self.current_player == "X" else "X"
        self.update_status()
        self.screen.update()

    def run(self):
        turtle.mainloop()


#  Запуск гри

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
