import tkinter as tk
import random
import math


class Ball:
    COLORS = ["red", "orange", "yellow", "green", "deep sky blue",
              "blue", "purple", "cyan", "magenta", "pink", "gold", "tomato"]

    def __init__(self, canvas, x, y):
        self.canvas = canvas

        self.x = x
        self.y = y

        self.radius = random.randint(8, 28)

        self.color = random.choice(self.COLORS)

        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 5)
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed

        self.id = canvas.create_oval(
            x - self.radius, y - self.radius,
            x + self.radius, y + self.radius,
            fill=self.color, outline=""
        )

    def move(self):

        self.x += self.dx
        self.y += self.dy
        self.canvas.move(self.id, self.dx, self.dy)

    def _update_position(self):
        self.canvas.coords(
            self.id,
            self.x - self.radius, self.y - self.radius,
            self.x + self.radius, self.y + self.radius
        )

    def change_color(self):
        self.color = random.choice(self.COLORS)
        self.canvas.itemconfig(self.id, fill=self.color)

    def check_walls(self, width, height):
        bounced = False

        if self.x - self.radius <= 0:
            self.x = self.radius
            self.dx = abs(self.dx)
            bounced = True
        elif self.x + self.radius >= width:
            self.x = width - self.radius
            self.dx = -abs(self.dx)
            bounced = True

        if self.y - self.radius <= 0:
            self.y = self.radius
            self.dy = abs(self.dy)
            bounced = True
        elif self.y + self.radius >= height:
            self.y = height - self.radius
            self.dy = -abs(self.dy)
            bounced = True

        if bounced:
            self._update_position()
            self.change_color()

        return bounced

    def collide(self, other):

        dx = other.x - self.x
        dy = other.y - self.y
        dist = math.hypot(dx, dy)

        if dist == 0:
            dist = 0.1  # уникаємо ділення на нуль

        if dist < self.radius + other.radius:
            nx = dx / dist
            ny = dy / dist

            dvx = self.dx - other.dx
            dvy = self.dy - other.dy
            p = dvx * nx + dvy * ny
            if p > 0:
                self.dx -= p * nx
                self.dy -= p * ny
                other.dx += p * nx
                other.dy += p * ny
                overlap = self.radius + other.radius - dist
                self.x -= nx * overlap / 2
                self.y -= ny * overlap / 2
                other.x += nx * overlap / 2
                other.y += ny * overlap / 2

                self._update_position()
                other._update_position()

                self.change_color()
                other.change_color()
                return True

        return False


class Game:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Bouncing Balls")
        self.root.geometry("800x600")
        self.balls = []
        self.collision_count = 0
        self.paused = False

        panel = tk.Frame(self.root)
        panel.pack(side=tk.TOP, fill=tk.X)

        self.info_label = tk.Label(panel, text="Кульок: 0 | Зіткнень: 0",
                                   font=("Arial", 11))
        self.info_label.pack(side=tk.LEFT, padx=10, pady=5)

        self.pause_btn = tk.Button(panel, text="Пауза", width=12,
                                   command=self.toggle_pause)
        self.pause_btn.pack(side=tk.LEFT, padx=5)

        clear_btn = tk.Button(panel, text="Очистити", width=12,
                              command=self.clear)
        clear_btn.pack(side=tk.LEFT, padx=5)
        self.canvas = tk.Canvas(self.root, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_click)
        self.animate()

    def on_click(self, event):
        ball = Ball(self.canvas, event.x, event.y)
        self.balls.append(ball)
        self.update_info()

    def toggle_pause(self):
        self.paused = not self.paused
        self.pause_btn.config(text="Продовжити" if self.paused else "Пауза")

    def clear(self):
        for ball in self.balls:
            self.canvas.delete(ball.id)
        self.balls.clear()
        self.collision_count = 0
        self.update_info()

    def update_info(self):
        self.info_label.config(
            text=f"Кульок: {len(self.balls)} | Зіткнень: {self.collision_count}"
        )

    def animate(self):
        if not self.paused:
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
            for ball in self.balls:
                ball.move()
                ball.check_walls(width, height)

            n = len(self.balls)
            for i in range(n):
                for j in range(i + 1, n):
                    if self.balls[i].collide(self.balls[j]):
                        self.collision_count += 1

            self.update_info()

        self.root.after(20, self.animate)

    def run(self):

        self.root.mainloop()


if __name__ == "__main__":
    Game().run()
