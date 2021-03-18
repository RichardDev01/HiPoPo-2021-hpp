import time
import math
import numpy as np

"""
Creeër de zeef -- een dynamische array van 2 tot N (dit kan een array van booleans zijn,
 of ints of wat dan ook waar je random access toe kan hebben en eenvoudig gebruikt kan
 worden om bepaalde elementen te "markeren").
Aangezien 1 geen priem is, zetten we k op 2.
"""

def zeef(n_size):
    n = n_size
    dynamic_array = [x for x in range(2, n)]
    # dynamic_array_bool = [True for _ in range(2, n)]
    dynamic_array_bool = [False]
    for number in range(2, n):
        for index, sta_num in enumerate(dynamic_array):
            if index == 0 or sta_num // number == 1:
                dynamic_array_bool.append(True)
                continue
            if sta_num % number == 0:
                # dynamic_array.remove(sta_num)
                dynamic_array_bool.append(False)
    # print(dynamic_array_bool)
    return dynamic_array_bool
    # return dynamic_array

def zeef_old(n_size):
    n = n_size
    dynamic_array = [x for x in range(2, n)]
    for number in range(2, n):
        for index, sta_num in enumerate(dynamic_array):
            if index == 0 or sta_num // number == 1:
                continue
            if sta_num % number == 0:
                dynamic_array.remove(sta_num)

    return dynamic_array

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



if __name__ == "__main__":
    n = 1000000000
    # start_zeef = time.time()
    # primes_zeef = zeef(n)
    # end_zeef = time.time()
    # elapse_time_zeef = end_zeef - start_zeef
    # print(f"boolZeef time = {elapse_time_zeef}")
    # # print(primes)
    #
    # start = time.time()
    # primes = zeef_old(n)
    # end = time.time()
    # elapse_time = end - start
    # print(f"zeef remove, time = {elapse_time}")
    # # print(primes)

    start = time.time()
    primes = zeef_new_hope(n)
    end = time.time()
    elapse_time = end - start
    print(f"zeef_new_hope {primes=}, time = {elapse_time}")

