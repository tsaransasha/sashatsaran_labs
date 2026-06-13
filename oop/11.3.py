def A(n):
    S = 1
    a1 = 1

    for i in range(2, n + 1):
        a1 = -a1 * (i - 1) / i
        S += a1
    return S


def B(n):
    S = 2

    for i in range(2, n + 1):
        an = 1 + 1 / i ** 2
        S *= an
    return S


def D(n):
    a1 = 1
    for i in range(n - 1):
        a1 = a1 + 1 / a1
        return a1


def E():
    d1 = 2
    d2 = 1
    for i in range()


if __name__ == "__main__":
    print(A(3))
    print(B(2))
    print(D(2))
