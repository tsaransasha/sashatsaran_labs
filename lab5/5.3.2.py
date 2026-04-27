from math import gcd


class Rational:
    def __init__(self, numerator, denominator=1):
        if denominator == 0:
            raise ValueError("Denominator cannot be zero")
        if isinstance(numerator, Rational):  # копіювання
            numerator, denominator = numerator.numerator, numerator.denominator
        g = gcd(numerator, denominator)
        self.numerator = numerator // g
        self.denominator = denominator // g

    def __add__(self, other):
        if isinstance(other, int):
            other = Rational(other)
        return Rational(
            self.numerator * other.denominator + other.numerator * self.denominator,
            self.denominator * other.denominator
        )

    def __radd__(self, other):
        if isinstance(other, int):
            return Rational(other) + self
        return NotImplemented

    def __str__(self):
        return f"{self.numerator}/{self.denominator}" if self.denominator != 1 else str(self.numerator)

    def __repr__(self):
        return str(self)

    def to_float(self):
        return self.numerator / self.denominator
