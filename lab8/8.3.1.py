import math

# a

print("Завдання а)")
x = float(input("Введіть x: "))
k = int(input("Введіть k (k >= 1): "))

xk = (x ** k) / k
print(f"x{k} =", xk)

# b

print("\n Завдання б)")
n = int(input("Введіть n: "))

pn = 1
for i in range(1, n + 1):
    pn = pn * (1 / math.factorial(i + 1))

print("Pn =", pn)

# в
print("\n Завдання в) ")
n = int(input("Введіть порядок матриці n: "))

matrix = []
for i in range(n):
    row = []
    for j in range(n):
        row.append(0)
    matrix.append(row)

for i in range(n):
    matrix[i][i] = 2
    if i + 1 < n:
        matrix[i][i + 1] = 3
    if i - 1 >= 0:
        matrix[i][i - 1] = 1

print("Матриця:")
for row in matrix:
    print(row)

m = []
for i in range(n):
    m.append(matrix[i][:])

det = 1
for i in range(n):
    if m[i][i] == 0:
        swapped = False
        for j in range(i + 1, n):
            if m[j][i] != 0:
                m[i], m[j] = m[j], m[i]
                det = det * (-1)
                swapped = True
                break
        if not swapped:
            det = 0
            break

    det = det * m[i][i]
    for j in range(i + 1, n):
        koef = m[j][i] / m[i][i]
        for l in range(i, n):
            m[j][l] = m[j][l] - koef * m[i][l]

print("Визначник =", round(det))

# г
print("\n Завдання г) ")
n = int(input("Введіть n: "))

a = [0] * (n + 1)
if n >= 1:
    a[1] = 0
if n >= 2:
    a[2] = 1
for k in range(3, n + 1):
    a[k] = a[k - 1] + k * a[k - 2]

sn = 0
for k in range(1, n + 1):
    sn = sn + (2 ** k) * a[k]

print("Sn =", sn)
# д

print("\n Завдання д) ")
x = float(input("Введіть x (в радіанах): "))
eps = float(input("Введіть точність eps: "))

summa = 0
chlen = x
n = 0

while abs(chlen) >= eps:
    summa = summa + chlen
    n = n + 1
    chlen = -chlen * x * x / ((2 * n) * (2 * n + 1))

print("sin(x) через ряд Тейлора =", summa)
print("sin(x) через math.sin =", math.sin(x))
print("Різниця =", abs(summa - math.sin(x)))
