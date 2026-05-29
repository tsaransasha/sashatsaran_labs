from math import gcd


class RationalError(ZeroDivisionError):

    def __init__(self, message="Знаменник не може дорівнювати нулю"):
        super().__init__(message)


class Rational:

    def __init__(self, numerator=0, denominator=1):

        if isinstance(numerator, str):
            # Рядковий варіант: 'n/d'
            parts = numerator.split('/')
            if len(parts) == 2:
                n, d = int(parts[0]), int(parts[1])
            else:
                n, d = int(parts[0]), 1
        else:
            n, d = int(numerator), int(denominator)

        if d == 0:
            raise RationalError()
        if d < 0:
            n, d = -n, -d
        common = gcd(abs(n), d)
        self._n = n // common
        self._d = d // common

    def __getitem__(self, key):
        if key == 'n':
            return self._n
        elif key == 'd':
            return self._d
        raise KeyError(f"Невідомий ключ '{key}'. Використовуйте 'n' або 'd'.")

    def __setitem__(self, key, value):
        if key == 'n':
            common = gcd(abs(int(value)), self._d)
            self._n = int(value) // common
            self._d = self._d // common
        elif key == 'd':
            if int(value) == 0:
                raise RationalError()
            d = int(value)
            if d < 0:
                self._n, d = -self._n, -d
            common = gcd(abs(self._n), d)
            self._n = self._n // common
            self._d = d // common
        else:
            raise KeyError(f"Невідомий ключ '{key}'. Використовуйте 'n' або 'd'.")

    def __call__(self):
        return self._n / self._d

    def __repr__(self):
        return f"Rational({self._n}/{self._d})"

    def __str__(self):
        return f"{self._n}/{self._d}" if self._d != 1 else str(self._n)

    def _coerce(self, other):
        if isinstance(other, int):
            return Rational(other, 1)
        if isinstance(other, Rational):
            return other
        return NotImplemented

    def __add__(self, other):
        other = self._coerce(other)
        if other is NotImplemented:
            return NotImplemented
        return Rational(self._n * other._d + other._n * self._d,
                        self._d * other._d)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        other = self._coerce(other)
        if other is NotImplemented:
            return NotImplemented
        return Rational(self._n * other._d - other._n * self._d,
                        self._d * other._d)

    def __rsub__(self, other):
        other = self._coerce(other)
        if other is NotImplemented:
            return NotImplemented
        return other.__sub__(self)

    def __mul__(self, other):
        other = self._coerce(other)
        if other is NotImplemented:
            return NotImplemented
        return Rational(self._n * other._n, self._d * other._d)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        other = self._coerce(other)
        if other is NotImplemented:
            return NotImplemented
        if other._n == 0:
            raise RationalError("Ділення на нуль: знаменник результату дорівнює нулю")
        return Rational(self._n * other._d, self._d * other._n)

    def __rtruediv__(self, other):
        other = self._coerce(other)
        if other is NotImplemented:
            return NotImplemented
        return other.__truediv__(self)

    def __eq__(self, other):
        other = self._coerce(other)
        if other is NotImplemented:
            return NotImplemented
        return self._n * other._d == other._n * self._d

    def __lt__(self, other):
        other = self._coerce(other)
        if other is NotImplemented:
            return NotImplemented
        return self._n * other._d < other._n * self._d


if __name__ == '__main__':
    print("=== Демонстрація класу Rational та RationalError ===\n")

    r1 = Rational(3, 4)
    r2 = Rational('5/6')
    r3 = Rational(10, -4)  # → -5/2
    print(f"r1 = {r1}")  # 3/4
    print(f"r2 = {r2}")  # 5/6
    print(f"r3 = {r3}")  # -5/2

    print(f"\nr1['n'] = {r1['n']}, r1['d'] = {r1['d']}")

    r1['n'] = 6
    print(f"Після r1['n'] = 6: r1 = {r1}")  # скорочення → 3/2
    print(f"\nr2() = {r2():.6f}")
    a = Rational(1, 2)
    b = Rational(1, 3)
    print(f"\na = {a}, b = {b}")
    print(f"a + b = {a + b}")
    print(f"a - b = {a - b}")
    print(f"a * b = {a * b}")
    print(f"a / b = {a / b}")
    print(f"a + 3  = {a + 3}")
    print(f"2 * a  = {2 * a}")
    print("\n--- Тест RationalError ---")
    try:
        bad = Rational(1, 0)
    except RationalError as e:
        print(f"RationalError спійманий: {e}")
    try:
        bad = Rational(5, 0)
    except ZeroDivisionError as e:
        print(f"ZeroDivisionError також спійманий (RationalError є нащадком): {e}")
    r_test = Rational(3, 5)
    try:
        r_test['d'] = 0
    except RationalError as e:
        print(f"RationalError при r['d']=0: {e}")
