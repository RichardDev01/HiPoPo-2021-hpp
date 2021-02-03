from typing import List
from timeit import default_timer as timer
import numpy as np

import sys
sys.setrecursionlimit(30000)

def merge_sort(xs: List[int]) -> None:
    """In place merge sort of array without recursive. The basic idea
    is to avoid the recursive call while using iterative solution.
    The algorithm first merge chunk of length of 2, then merge chunks
    of length 4, then 8, 16, .... , until 2^k where 2^k is large than
    the length of the array
    """

    unit = 1
    while unit <= len(xs):
        h = 0
        for h in range(0, len(xs), unit * 2):
            l, r = h, min(len(xs), h + 2 * unit)
            mid = h + unit
            # merge xs[h:h + 2 * unit]
            p, q = l, mid
            while p < mid and q < r:
                # use <= for stable merge merge
                if xs[p] <= xs[q]:
                    p += 1
                else:
                    tmp = xs[q]
                    xs[p + 1: q + 1] = xs[p:q]
                    xs[p] = tmp
                    p, mid, q = p + 1, mid + 1, q + 1

        unit *= 2


def merge_arrays(array1: List[int], array2: List[int]) -> List[int]:
    """Recursively merge two arrays into one sorted array"""
    if len(array1) == len(array2) == 0: # done when both arrays are empty
        return []
    else:
        if len(array1) == 0: # if either array is empty
            head, *tail = array2
            return [head] + merge_arrays(array1, tail) # merge the remainder of the non-empty list
        elif len(array2) == 0: # idem for the other array
            head, *tail = array1
            return [head] + merge_arrays(tail, array2)
        else: # when both still have elements
            head1, *tail1 = array1
            head2, *tail2 = array2
            if head1 < head2: # select the smallest
                return [head1] + merge_arrays(tail1, array2) # and merge with the remainder
            else:
                return [head2] + merge_arrays(array1, tail2) # idem for when array 2 had the smaller element


def recursive_merge_sort(data: List[int]) -> List[int]:
    """Recursive merge sort implementation for sorting arrays"""
    if len(data) == 1: # arrays with 1 element are sorted
        return data
    else:
        middle = int(len(data)/2) # find the middle (round down if len(data) is odd)
        first, second = data[:middle], data[middle:] # split the list in half
        return merge_arrays(recursive_merge_sort(first), recursive_merge_sort(second)) # merge_sort both arrays, and merge them into the result

randomlist1k = list(np.random.randint(low=0, high=100, size=1000))
randomlist1k2 = list(np.random.randint(low=0, high=100, size=1000))

randomlist10k = list(np.random.randint(low=0, high=100, size=10000))
randomlist10k2 = list(np.random.randint(low=0, high=100, size=10000))

randomlist30k = list(np.random.randint(low=0, high=100, size=30000))


start = timer()
merge_sort(randomlist1k)
elapsed_time = timer() - start
print('merge_sort(randomlist1k)', elapsed_time)

start = timer()
merge_arrays(randomlist1k,randomlist1k2)
elapsed_time = timer() - start
print('merge_arrays(randomlist1k - randomlist1k2)', elapsed_time)

start = timer()
merge_sort(randomlist10k)
elapsed_time = timer() - start
print('merge_sort(randomlist10k)', elapsed_time)

start = timer()
merge_sort(randomlist30k)
elapsed_time = timer() - start
print('merge_sort(randomlist30k)', elapsed_time)
