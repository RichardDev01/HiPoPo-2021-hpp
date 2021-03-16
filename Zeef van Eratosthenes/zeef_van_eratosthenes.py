import time
"""
Creeër de zeef -- een dynamische array van 2 tot N (dit kan een array van booleans zijn,
 of ints of wat dan ook waar je random access toe kan hebben en eenvoudig gebruikt kan
 worden om bepaalde elementen te "markeren").
Aangezien 1 geen priem is, zetten we k op 2.
"""

def zeef(n_size):
    n = n_size
    dynamic_array = [x for x in range(2, n)]
    for number in range(2, n):
        for index, sta_num in enumerate(dynamic_array):
            if index == 0 or sta_num // number == 1:
                continue
            if sta_num % number == 0:
                try:
                    dynamic_array.remove(sta_num)
                except:
                    continue
    return dynamic_array

if __name__ == "__main__":
    n = 1000000000
    start = time.time()
    primes = zeef(n)
    end = time.time()
    elapse_time = end - start
    print(f"time = {elapse_time}")


