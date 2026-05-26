
import math
import re


# Клас Rational
class Rational:
    def __init__(self, numerator=0, denominator=1):
        if denominator == 0:
            raise ValueError("Denominator cannot be zero")
        if denominator < 0:
            numerator = -numerator
            denominator = -denominator
        self._numerator = numerator
        self._denominator = denominator
        self._reduce()

    def _gcd(self, a, b):
        while b:
            a, b = b, a % b
        return abs(a)

    def _reduce(self):
        if self._numerator == 0:
            self._denominator = 1
            return
        gcd = self._gcd(self._numerator, self._denominator)
        self._numerator //= gcd
        self._denominator //= gcd

    def numerator(self):
        return self._numerator

    def denominator(self):
        return self._denominator

    def __str__(self):
        if self._denominator == 1:
            return f"{self._numerator}"
        return f"{self._numerator}/{self._denominator}"

    def __repr__(self):
        return f"Rational({self._numerator}, {self._denominator})"

    def __float__(self):
        return self._numerator / self._denominator

    def __add__(self, other):
        if isinstance(other, int):
            other = Rational(other, 1)
        if isinstance(other, Rational):
            new_num = self._numerator * other._denominator + other._numerator * self._denominator
            new_den = self._denominator * other._denominator
            return Rational(new_num, new_den)
        return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        res = self.__add__(other)
        self._numerator, self._denominator = res._numerator, res._denominator
        return self

    def __eq__(self, other):
        if isinstance(other, Rational):
            return self._numerator == other._numerator and self._denominator == other._denominator
        elif isinstance(other, int):
            return self._numerator == other and self._denominator == 1
        return NotImplemented

    def __hash__(self):
        return hash((self._numerator, self._denominator))


class RationalListIterator:
    def __init__(self, items):
        self._items = items
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._items):
            raise StopIteration
        result = self._items[self._index]
        self._index += 1
        return result


class RationalList:
    def __init__(self, items=None):
        self._items = []
        if items is not None:
            for item in items:
                self.append(item)

    def append(self, item):
        if isinstance(item, Rational):
            self._items.append(item)
        elif isinstance(item, int):
            self._items.append(Rational(item, 1))
        else:
            raise TypeError(f"Only Rational or int allowed, got {type(item)}")

    def __getitem__(self, index):
        return self._items[index]

    def __setitem__(self, index, value):
        if isinstance(value, Rational):
            self._items[index] = value
        elif isinstance(value, int):
            self._items[index] = Rational(value, 1)
        else:
            raise TypeError(f"Only Rational or int allowed, got {type(value)}")

    def __len__(self):
        return len(self._items)

    def __add__(self, other):
        new_list = RationalList(self._items)
        if isinstance(other, RationalList):
            for item in other._items:
                new_list.append(item)
        elif isinstance(other, (Rational, int)):
            new_list.append(other)
        else:
            raise TypeError(f"Cannot concatenate RationalList with {type(other)}")
        return new_list

    def __radd__(self, other):
        if isinstance(other, (Rational, int)):
            new_list = RationalList()
            new_list.append(other)
            for item in self._items:
                new_list.append(item)
            return new_list
        return NotImplemented

    def __iadd__(self, other):
        if isinstance(other, RationalList):
            for item in other._items:
                self.append(item)
        elif isinstance(other, (Rational, int)):
            self.append(other)
        else:
            raise TypeError(f"Cannot add {type(other)} to RationalList")
        return self

    def __str__(self):
        return "[" + ", ".join(str(item) for item in self._items) + "]"

    def __repr__(self):
        return f"RationalList({self._items})"

    def sum(self):
        total = Rational(0, 1)
        for item in self._items:
            total += item
        return total

    def __iter__(self):
        # Видаляємо дублікати за допомогою set, потім сортуємо
        unique_items = list(set(self._items))
        sorted_items = sorted(unique_items, key=lambda x: (x.denominator(), x.numerator()), reverse=True)
        return RationalListIterator(sorted_items)


def read_rationals_from_file(filename):
    rational_list = RationalList()

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            words = line.strip().split()
            for word in words:
                if '/' in word:
                    parts = word.split('/')
                    if len(parts) == 2:
                        try:
                            num = int(parts[0])
                            den = int(parts[1])
                            rational_list.append(Rational(num, den))
                        except ValueError:
                            pass
                else:
                    try:
                        num = int(word)
                        rational_list.append(Rational(num, 1))
                    except ValueError:
                        pass

    return rational_list


def main():
    input_files = ["input01.txt"]

    for filename in input_files:
        try:
            rational_list = read_rationals_from_file(filename)

            if len(rational_list) == 0:
                print(f"{filename}: немає чисел у файлі")
                continue

            total = rational_list.sum()
            print(f"{filename}:")
            print(f"  Послідовність : {', '.join(str(item) for item in rational_list)}")
            print(f"  Кількість чисел : {len(rational_list)}")
            print(f"  Кількість унікальних чисел: {len(set(rational_list._items))}")
            print(f"  Сума: {total}")
            if float(total) != int(float(total)):
                print(f"  Сума (десятковий вигляд): {float(total):.6f}")
            print()

        except FileNotFoundError:
            print(f"{filename}: файл не знайдено\n")
        except Exception as e:
            print(f"{filename}: помилка - {e}\n")


if __name__ == "__main__":
    main()