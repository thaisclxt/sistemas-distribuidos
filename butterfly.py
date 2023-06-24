# Algoritmo para o cálculo da integral pelo método butterfly
from mpi4py import MPI
import datetime

# Comunicador básico que envolve todos os processos, sempre deve existir
comm = MPI.COMM_WORLD
size = comm.Get_size()  # Pega o número de processos
rank = comm.Get_rank()  # Pega o rank (ID) do processo


def f(x):
    return 5 * x**3 + 3 * x**2 + 4 * x + 20


def calcula_integral(x0, xn, n):
    start_time = datetime.datetime.now()

    if rank == 0:
        numero = comm.bcast(n, root=0)
    else:
        numero = comm.bcast(None, root=0)

    parcela = numero // size
    h = (xn - x0) / numero
    x = x0 + h + h * rank * parcela

    soma = 0.0

    for _ in range(parcela):
        soma += f(x)
        x += h

    metade = size

    while rank < metade and metade > 1:
        metade /= 2
        resultado = soma

        if rank >= metade:
            comm.send(resultado, dest=rank-metade)
        else:
            resultado = comm.recv(source=rank+metade)
            soma += resultado

    if rank == 0:
        resultado = h * ((f(x0) + f(xn)) / 2 + soma)

        end_time = datetime.datetime.now()
        time_diff = end_time - start_time
        execution_time = time_diff.total_seconds()

        print("O resultado da integral da função f é:", soma)
        print("Tempo de execução em segundos:", execution_time)


def main():
    x0 = 0
    xn = 1000000
    n = 10000000

    if n == 0:
        print("Divisão por zero")
    if n < 0:
        print("Intervalo inválido")
    else:
        calcula_integral(x0, xn, n)


if __name__ == "__main__":
    main()
