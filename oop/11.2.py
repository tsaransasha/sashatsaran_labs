def A(n):
    S = 0
    for i in range(1, n + 1):
        S = S + i
    return S


if __name__ == "__main__":
    print(A(5))
