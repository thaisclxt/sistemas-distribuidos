# Algoritmo sequencial pelo método do trapézio
import datetime


def f(x):
    return 5 * x**3 + 3 * x**2 + 4 * x + 20


def calcula_integral(x0, xn, n):
    h = (xn - x0) / n
    x = x0 + h

    soma = 0.0

    for _ in range(n-1):
        soma += f(x)
        x += h

    resultado = h * ((f(x0) + f(xn)) / 2 + soma)

    print("O resultado da integral da função f é:", resultado)


def main():
    x0 = 0
    xn = 1000000
    n = 10000000

    start_time = datetime.datetime.now()

    if n == 0:
        print("Divisão por zero")
    elif n < 0:
        print("Intervalo inválido")
    else:
        calcula_integral(x0, xn, n)

    end_time = datetime.datetime.now()
    time_diff = (end_time - start_time)
    execution_time = time_diff.total_seconds()

    print("Tempo de execução em segundos:", execution_time)


if __name__ == "__main__":
    main()
