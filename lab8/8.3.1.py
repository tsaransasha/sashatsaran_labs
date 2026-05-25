import math


# а
def recursive_power(x, power):
    if power == 0:
        return 1
    return x * recursive_power(x, power - 1)


def sequence_generator_a(x, k):
    for i in range(1, k + 1):
        yield recursive_power(x, i) / i


#b

def product_recursive(n):
    if n == 1:
        return 1 / (1 + 1)
    return product_recursive(n - 1) * (1 / (n + 1))


def product_history_generator(n):
    current_product = 1.0
    for i in range(1, n + 1):
        current_product *= (1 / (i + 1))
        yield current_product


#c

def determinant_recursive(n):
    if n == 1:
        return 2
    if n == 2:
        return 1
    return 2 * determinant_recursive(n - 1) - 3 * determinant_recursive(n - 2)


def determinant_generator(n):
    for i in range(1, n + 1):
        yield determinant_recursive(i)


# d
def calculate_a_recursive(k):
    if k == 1:
        return 0
    if k == 2:
        return 1
    return calculate_a_recursive(k - 1) + k * calculate_a_recursive(k - 2)


def sum_terms_generator(n):
    for k in range(1, n + 1):
        yield (2 ** k) * calculate_a_recursive(k)


# е

def taylor_sin_generator(x):
    term = x
    m = 0
    yield term
    while True:
        m += 1
        term = term * (-x ** 2) / ((2 * m) * (2 * m + 1))
        yield term


def accumulate_taylor_recursive(gen, eps, current_sum=0.0):
    term = next(gen)
    current_sum += term
    if abs(term) < eps:
        return current_sum
    return accumulate_taylor_recursive(gen, eps, current_sum)


if __name__ == "__main__":
    # Тест А
    x_a, k_a = 2.0, 5
    elements_a = [elem for elem in sequence_generator_a(x_a, k_a)]
    print(f"Пункт а) Для x={x_a}, k={k_a}:")
    print(f"  -> Усі згенеровані елементи: {elements_a}")
    print(f"  -> Шуканий k-й елемент: {elements_a[-1]}")
    print("  " *50)

    # Тест B
    n_b = 4
    print(f"Пункт b) Для n={n_b}:")
    print(f"  -> Результат рекурсії P_n: {product_recursive(n_b)}")
    print(f"  -> Етапи добутку (генератор): {list(product_history_generator(n_b))}")
    print("  " * 50)

    # Тест C
    n_c = 5
    print(f"Пункт c) Визначник порядку n={n_c}:")
    print(f"  -> Результат рекурсії: {determinant_recursive(n_c)}")
    print(f"  -> Визначники від 1 до {n_c} ступеня: {list(determinant_generator(n_c))}")
    print("  " * 50)

    # Тест D
    n_d = 4
    total_sum_d = sum(sum_terms_generator(n_d))
    print(f"Пункт d) Для n={n_d}:")
    print(f"  -> Обчислена сума S_n: {total_sum_d}")
    print("  " * 50)

    # Тест E
    x_e, eps_e = 1.0, 1e-6
    sin_gen = taylor_sin_generator(x_e)
    calculated_sin = accumulate_taylor_recursive(sin_gen, eps_e)
    math_sin = math.sin(x_e)
    print(f"Пункт e) Розклад sin({x_e}) з точністю {eps_e}:")
    print(f"  -> Через рекурсію + генератор: {calculated_sin}")
    print(f"  -> Значення з бібліотеки math: {math_sin}")
    print(f"  -> Абсолютна похибка:          {abs(calculated_sin - math_sin)}")
    print("  " * 50)
