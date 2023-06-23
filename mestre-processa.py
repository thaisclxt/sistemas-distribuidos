# Algoritmo para o cálculo da integral onde o mestre processa com comunicação coletiva
from mpi4py import MPI
import datetime


# Comunicador básico que envolve todos os processos, sempre deve existir
comm = MPI.COMM_WORLD
size = comm.Get_size()  # Pega o número de processos
rank = comm.Get_rank()  # Pega o rank (ID) do processo


def f(x):
    return 5 * x**3 + 3 * x**2 + 4 * x + 20


def mestre_calcula_integral(x0, xn, n):
    intervalo_por_processo = comm.bcast(n // size, root=0)
    h = comm.bcast((xn - x0) / n, root=0)
    x = comm.bcast(x0 + h, root=0)

    soma = 0.0
    soma = comm.reduce(soma, op=MPI.SUM, root=0)

    for _ in range(1, intervalo_por_processo + 1):
        soma += f(x)
        x += h

    resultado = h * ((f(x0) + f(xn)) / 2 + soma)

    print("O resultado da integral da função f é:", resultado)


def escravo_calcula_integral():
    intervalo = comm.bcast(None, root=0)
    h = comm.bcast(None, root=0)
    x = comm.bcast(None, root=0) + h * rank * intervalo

    soma = 0.0
    for _ in range(1, intervalo + 1):
        soma += f(x)
        x += h

    comm.reduce(soma, op=MPI.SUM, root=0)


def main():
    x0 = 0
    xn = 1000000
    n = 10000000

    if rank == 0:  # Mestre
        if n == 0:
            print("Divisão por zero")
        elif n < 0:
            print("Intervalo inválido")
        else:
            start_time = datetime.datetime.now()

            mestre_calcula_integral(x0, xn, n)

            end_time = datetime.datetime.now()
            time_diff = end_time - start_time
            execution_time = time_diff.total_seconds()

            print("Tempo de execução em segundos:", execution_time)

    else:  # Escravo
        escravo_calcula_integral()


if __name__ == "__main__":
    main()
