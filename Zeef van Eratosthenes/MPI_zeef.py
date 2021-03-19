# cd PycharmProjects/HiPoPo-2021-hpp/Zeef\ van\ Eratosthenes/
# mpiexec -n 4 python3 MPI_zeef.py
#
# mpiexec -n [mpi nodes] python3 MPI_zeef.py [n size] [multi processing cores] [stripes|chunks = c or s]


import time
import math
from sys import argv
import numpy as np
from mpi4py import MPI
import concurrent.futures
from functools import reduce


def zeef_classic(n_size):
    """
    Deze functie returned een lijst met prime numbers die in de range van 2 tot n voorkomen
    :param n_size: grote van de lijst
    :return: lijst met prime nummers
    """
    dynamic_array = [x for x in range(2, n_size)]
    for number in range(2, n_size):
        for index, sta_num in enumerate(dynamic_array):
            if index == 0 or sta_num // number == 1:
                continue
            if sta_num % number == 0:
                dynamic_array.remove(sta_num)

    return dynamic_array


def determin_prime_from_list(precalculated_primes_list, unchecked_list):
    """
    deze functie returned een lijst met prime nummers aan de hand van de niet gecheckte lijst en de voor bepaalde prime nummers
    :param precalculated_primes_list: lijst met voor berekende primes
    :param unchecked_list: lijst van getallen die nog niet gecontroleerd zijn
    :return: lijst met prime nummers
    """
    calculated_primes_list = []
    for number in unchecked_list:
        for index, known_prime in enumerate(precalculated_primes_list):
            if number % known_prime == 0:
                break
            if index == len(precalculated_primes_list)-1:
                calculated_primes_list.append(number)
    return calculated_primes_list


def determin_prime_from_list_mp(unchecked_list):
    """
    deze functie returned een lijst met prime nummers aan de hand van de niet gecheckte lijst en de voor bepaalde prime nummers
    :param unchecked_list: lijst van getallen die nog niet gecontroleerd zijn
    :return: lijst met prime nummers
    """
    calculated_primes_list = []
    precalculated_primes_list = precalculated_primes  # Global var in dit geval
    for number in unchecked_list:
        for index, known_prime in enumerate(precalculated_primes_list):
            if number % known_prime == 0:
                break
            if index == len(precalculated_primes_list)-1:
                calculated_primes_list.append(number)
    return calculated_primes_list


if __name__ == "__main__":
    n = int(argv[1])  # grote van de lijst
    procces_in_nodes = int(argv[2])  # aantal processen in een node
    stripes_or_chunks = str(argv[3])  # keuze tussen stripes of chunks

    # Sequentieel -----------------
    '''
    Ik weet dat elke mpi node het berekent, maar dan doet elke nodes iets ipv idle staan
    '''

    list_of_numbers = [x for x in range(2, n)]

    root_n = math.floor(math.sqrt(n))

    precalculated_primes = zeef_classic(root_n)

    # MPI -------

    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()

    # Starten van de timer
    if rank == 0:
        start = time.time()

    # grote lijst opdelen in Stripes of in Chunks voor de nodes
    if stripes_or_chunks == "s":
        working_list = list(list_of_numbers[i::size] for i in range(size))[rank]  # split into stripes
    elif stripes_or_chunks == "c":
        working_list = np.array_split(list_of_numbers, size)[rank]  # split into chunks
    else:
        raise ("error, not stripes or chunks, use 's' or 'c'")

    # Node lijst opdelen in chunks voor multi processing
    working_list_bit = np.array_split(working_list, procces_in_nodes)

    # Multi processing gedeelte
    with concurrent.futures.ProcessPoolExecutor(max_workers=procces_in_nodes) as executor:
        results = executor.map(determin_prime_from_list_mp, working_list_bit)

    primes_node = reduce(lambda x, y: x+y, list(results))

    # # Pre multi processing code
    # primes_node = determin_prime_from_list(precalculated_primes,working_list)

    # # Debug print statements
    # print(f"{rank=} {precalculated_primes=} {working_list=}")
    # print(f"{rank=} \n{working_list=}\n{primes_node=}\n")

    '''
    Verwerkte code van stack overflow
    https://stackoverflow.com/a/38008452
    '''
    local_array = primes_node
    # print("rank: {}, local_array: {}".format(rank, local_array))

    sendbuf = np.array(local_array)

    # Collect local array sizes using the high-level mpi4py gather
    sendcounts = np.array(comm.gather(len(sendbuf), 0))
    if rank == 0:
        # print("sendcounts: {}, total: {}".format(sendcounts, sum(sendcounts)))
        recvbuf = np.empty(sum(sendcounts), dtype=int)
    else:
        recvbuf = None

    comm.Gatherv(sendbuf=sendbuf, recvbuf=(recvbuf, sendcounts), root=0)

    if rank == 0:
        concat_prime = precalculated_primes+recvbuf.tolist()
        end = time.time()
        elapse_time = end - start
        # print(f"time = {elapse_time}\n{concat_prime}")
        print(f"N list = {n}\nNumber of MPI Nodes= {size}\nNumber of procceses per Node = {procces_in_nodes}\ntime = {elapse_time}\nnumber of prime values= {len(concat_prime)}")

