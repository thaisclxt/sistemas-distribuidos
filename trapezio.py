# Algoritmo em paralelo pelo método do trapézio com comunicação coletiva
from mpi4py import MPI
import datetime


# Comunicador básico que envolve todos os processos, sempre deve existir
comm = MPI.COMM_WORLD
size = comm.Get_size()  # Pega o número de processos
rank = comm.Get_rank()  # Pega o rank (ID) do processo


def f(x):
    return 5 * x**3 + 3 * x**2 + 4 * x + 20


# Calcula a integral pelo método do trapézio
def calcula_integral(x0, xn, n):
    if n == 0:
        if rank == 0:
            print("Divisão por zero")
        return

    elif n < 0:
        if rank == 0:
            print("Intervalo inválido")
        return

    h = (xn - x0) / n
    n_local = n // size
    x0_local = x0 + rank * n_local * h
    xn_local = x0_local + n_local * h

    soma_local = 0.0

    # Calcula a soma local
    for i in range(n_local - 1):
        x = x0_local + i * h
        soma_local += f(x)

    # Realiza a redução da soma local para obter o resultado final
    soma_global = comm.reduce(soma_local, op=MPI.SUM, root=0)

    # Faz o cálculo do resultado parcial de cada processo
    resultado_parcial = h * ((f(x0_local) + f(xn_local)) / 2 + soma_local)

    # Exibe o resultado parcial em cada processo
    print("Processo", rank, "- Resultado parcial:", resultado_parcial)

    if rank == 0:
        resultado = h * ((f(x0) + f(xn)) / 2 + soma_global)
        print("O resultado da integral da função f é:", resultado)


if __name__ == "__main__":
    # Apenas o processo mestre define os parâmetros da integral e o escravo recebe através da transmissão coletiva
    if rank == 0:  # Mestre
        x0 = 0
        xn = 1000000
        n = 10000000
    else:  # Escravo
        x0 = None
        xn = None
        n = None

    # Início da medição do tempo de execução
    start_time = datetime.datetime.now()

    # Broadcast dos parâmetros da integral para todos os processos
    x0 = comm.bcast(x0, root=0)
    xn = comm.bcast(xn, root=0)
    n = comm.bcast(n, root=0)

    calcula_integral(x0, xn, n)

    # Fim da medição do tempo de execução
    end_time = datetime.datetime.now()
    time_diff = (end_time - start_time)
    execution_time = time_diff.total_seconds()

    total_execution_time = comm.reduce(execution_time, op=MPI.SUM, root=0)

    print("Processo", rank, "- Tempo de execução em segundos:", execution_time)

    if rank == 0:
        average_execution_time = total_execution_time / size
        print("Média do tempo de execução em segundos:", average_execution_time)
