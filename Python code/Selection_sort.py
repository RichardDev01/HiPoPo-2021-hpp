from typing import List
from timeit import default_timer as timer
import numpy as np
import random
import sys
sys.setrecursionlimit(30000)

# https://en.wikipedia.org/wiki/Selection_sort
def selection_sort(data: List[int]) -> None:
    """Sort an array using selection sort"""
    # loop over len(data) -1 elements
    for index1 in range(len(data)-1):
        smallest = index1 # first index of remaining array

        # loop to find index of smallest element
        for index2 in range(index1 + 1, len(data)):
            if data[index2] < data[smallest]:
                smallest = index2

        # swap smallest element into position
        data[smallest], data[index1] = data[index1], data[smallest]


def recursive_selection_sort(data: List[int]) -> None:
    # Lists with less than one element are sorted
    if len(data) <= 1:
        return data
    else:
        smallest = min(data)    # find the smallest element in the list
        data.remove(smallest)   # remove from the list
        return [smallest] + recursive_selection_sort(data) # put on front of to be sorted remainder


randomlist1k  = list(np.random.randint(low=0, high=100, size=1000))
randomlist10k = list(np.random.randint(low=0, high=100, size=10000))
randomlist30k = list(np.random.randint(low=0, high=100, size=30000))


start = timer()
selection_sort(randomlist1k)
elapsed_time = timer() - start
print('selection_sort(randomlist1k)', elapsed_time)

start = timer()
recursive_selection_sort(randomlist1k)
elapsed_time = timer() - start
print('recursive_selection_sort(randomlist1k)', elapsed_time, '\n')

start = timer()
selection_sort(randomlist10k)
elapsed_time = timer() - start
print('selection_sort(randomlist10k)', elapsed_time)


start = timer()
selection_sort(randomlist30k)
elapsed_time = timer() - start
print('selection_sort(randomlist30k)', elapsed_time)


'''
Maakt het voor de complexiteit (Big O) van een algoritme uit of je een iteratieve of een recursieve versie beschouwd?

Recursie is vele maten sneller dan iteratief

'''