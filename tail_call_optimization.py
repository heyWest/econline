def factorial(n, acc=1):
    if n == 0:
        return acc
    return factorial(n - 1, acc * n)

