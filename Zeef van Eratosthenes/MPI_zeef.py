'''
cd PycharmProjects/HiPoPo-2021-hpp/Zeef\ van\ Eratosthenes/
mpiexec -n 4 python3 MPI_zeef.py

'''

import time
import math
import numpy as np
from mpi4py import MPI


def zeef_new_hope(n_size):
    dynamic_array_bool = [True for _ in range(n_size+1)]
    # dynamic_array_bool = np.full(n_size +1, True, dtype=bool) \\ dit is langzamer :C
    k = 2
    # root_n =math.ceil(math.sqrt(n_size))
    # for index, prime in enumerate(range(dynamic_array_bool[k: root_n])):
    dynamic_array_bool[0] = False
    dynamic_array_bool[1] = False
    while (k * k < n_size):
        if (dynamic_array_bool[k] == True):
            # updating all the multiples
            for i in range(k ** 2, n_size + 1, k):
                dynamic_array_bool[i] = False
        k += 1
    return np.count_nonzero(dynamic_array_bool)

def zeef_classic(n_size):
    n = n_size
    dynamic_array = [x for x in range(2, n)]
    for number in range(2, n):
        for index, sta_num in enumerate(dynamic_array):
            if index == 0 or sta_num // number == 1:
                continue
            if sta_num % number == 0:
                dynamic_array.remove(sta_num)

    return dynamic_array

def determin_prime_from_list(precalculated_primes_list, unchecked_list):
    calculated_primes_list = []
    for number in unchecked_list:
        for index, known_prime in enumerate(precalculated_primes_list):
            if number % known_prime == 0:
                break
            if index == len(precalculated_primes_list)-1:
                calculated_primes_list.append(number)
    return calculated_primes_list



if __name__ == "__main__":
    n = 100000
    procces_in_nodes = 4

    # Sequentieel -----------------

    list_of_numbers = [x for x in range(2, n)]

    root_n = math.floor(math.sqrt(n))

    precalculated_primes = zeef_classic(root_n)

    # MPI -------

    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()

    if rank == 0:
        start = time.time()

    # working_list = list(list_of_numbers[i::size] for i in range(size))[rank] # split into stripes
    working_list = np.array_split(list_of_numbers, size)[rank] # split into chunks

    primes_node = determin_prime_from_list(precalculated_primes,working_list)

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
        print(f"time = {elapse_time}\n{len(concat_prime)}")

