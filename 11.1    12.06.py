def A(x, n):
    if n < 1:
        raise ValueError
    x1 = x
    for k in range(2, n + 1):
        x1 = x1 * x * (k - 1) / k
        return x1


if __name__ == "__main__":
    print(A(2, 4))
