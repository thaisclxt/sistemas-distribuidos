# Algoritmo sequencial pelo método do trapézio
import datetime


def f(x):
    return 5 * x**3 + 3 * x**2 + 4 * x + 20


def calcula_integral(x0, xn, n):
    if n == 0:
        print("Divisão por zero")
        return

    elif n < 0:
        print("Intervalo inválido")
        return

    h = (xn - x0) / n
    soma = 0.0

    for i in range(1, n):
        x = x0 + i * h
        soma += f(x)

    resultado = h * ((f(x0) + f(xn)) / 2 + soma)

    return resultado


if __name__ == "__main__":
    x0 = 0
    xn = 1000000
    n = 10000000

    start_time = datetime.datetime.now()

    resultado_sequencial = calcula_integral(x0, xn, n)

    end_time = datetime.datetime.now()
    time_diff = (end_time - start_time)
    execution_time = time_diff.total_seconds()

    print("O resultado da integral da função f (sequencial) é:", resultado_sequencial)
    print("Tempo de execução em segundos (sequencial):", execution_time)
