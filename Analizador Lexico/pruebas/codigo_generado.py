def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


if __name__ == "__main__":
    n = 10
    print("Serie de Fibonacci (recursiva) ")
    print("Termino: ")
    print(n)
    print("Valor: ")
    print(fibonacci(n))