from abc import ABC, abstractmethod

HUMANITARIAN = "humanitarian"
NATURAL = "natural"
NATURAL_HUMANITARIAN = "natural-humanitarian"


class Activity(ABC):

    @abstractmethod
    def accept(self, visitor):
        pass


class TeachActivity(Activity):

    def __init__(self, profile, credits):
        self.profile = profile
        self.credits = credits

    def accept(self, visitor):
        visitor.visit_teach(self)


class PayActivity(Activity):

    def __init__(self, target, amount):
        self.target = target  # hostel / canteen
        self.amount = amount

    def accept(self, visitor):
        visitor.visit_pay(self)


class ObtainActivity(Activity):

    def __init__(self, source, amount):
        self.source = source  # scholarship / help
        self.amount = amount

    def accept(self, visitor):
        visitor.visit_obtain(self)


class Visitor(ABC):
    def visit_teach(self, element):
        pass

    def visit_pay(self, element):
        pass

    def visit_obtain(self, element):
        pass


class Student(Visitor):


    def __init__(self, direction, required_credits, money):
        self.direction = direction
        self.required_credits = required_credits
        self.money = money
        self.credits = 0
        self.expelled = False

    def _can_master(self, profile):

        if self.direction == NATURAL_HUMANITARIAN:
            return True
        return self.direction == profile

    def visit_teach(self, element):
        if self.expelled:
            return

        if self._can_master(element.profile):
            self.credits += element.credits

    def visit_obtain(self, element):
        if self.expelled:
            return

        self.money += element.amount

    def visit_pay(self, element):
        if self.expelled:
            return
        if self.money >= element.amount:
            self.money -= element.amount
        else:

            self.expelled = True

    def has_diploma(self):
        return (not self.expelled) and (self.credits >= self.required_credits)


def parse(filename):
    """Зчитує файл і повертає (student, activities)."""
    with open(filename, encoding="utf-8") as f:
        lines = [line.split() for line in f if line.strip()]

    direction = lines[0][0]
    required_credits = int(lines[1][0])
    start_money = int(lines[2][0])

    student = Student(direction, required_credits, start_money)

    activities = []
    for verb, prop, value in (parts for parts in lines[3:]):
        value = int(value)
        if verb == "teach":
            activities.append(TeachActivity(prop, value))
        elif verb == "pay":
            activities.append(PayActivity(prop, value))
        elif verb == "obtain":
            activities.append(ObtainActivity(prop, value))

    return student, activities


def simulate(filename):
    student, activities = parse(filename)
    for activity in activities:  # студент "відвідує" кожен крок свого життя
        activity.accept(student)
    return student


def main():
    import os

    folder = os.path.dirname(os.path.abspath(__file__))
    for i in range(1, 15):
        filename = os.path.join(folder, f"input{i:02d}.txt")
        if not os.path.exists(filename):
            continue

        student = simulate(filename)
        answer = "отримає диплом" if student.has_diploma() else "НЕ отримає диплом"
        print(f"input{i:02d}.txt | напрям: {student.direction:>21} | "
              f"кредити: {student.credits:>4}/{student.required_credits} | "
              f"гроші: {student.money:>7} | "
              f"{'відрахований' if student.expelled else 'навчається ':>12} -> "
              f"студент {answer}")


if __name__ == "__main__":
    main()
