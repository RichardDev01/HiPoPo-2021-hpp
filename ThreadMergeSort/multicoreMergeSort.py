from typing import List
import time
import numpy as np
import concurrent.futures

#Studentnummer
np.random.seed(1762581)

import sys
sys.setrecursionlimit(30000)


def merge_sort(xs: List[int]):
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
    return xs

def split_list_array_merge(mainlist):
    array1 = mainlist[0]
    array2 = mainlist[1]
    return merge_arrays(array1,array2)

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


def chunk_slicer(mainlist: List[int], n_chunks:int = 4) -> List[int]:
    return list(mainlist[i::n_chunks] for i in range(n_chunks))


def create_lists_of_two(mainlist):
    index = 0
    values = mainlist
    set_lists = []
    for _ in range(0, len(values), 2):
        set_lists.append([values[index], values[index+(int(len(values)/2))]])
        index += 1
    return set_lists


def process_join_sort(pre_results):
    values = list(pre_results)
    # print(values)

    if len(values) >= 2:
        combined_List = create_lists_of_two(values)

        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = executor.map(split_list_array_merge, combined_List)
        return process_join_sort(results)
    else:
        return values


if __name__ == '__main__':
    randomlist100 = list(np.random.randint(low=0, high=100, size=2000))
    unsorted_list = [0, 11, 8, 15, 16, 2, 21, 25]

    n_cores = 4

    chunks = chunk_slicer(randomlist100, n_cores)
    start = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(merge_sort, chunks)

    process_join_sort(results)
    # print(list(process_join_sort(results)), 'end')
    finish = time.perf_counter()

    print(f'Finished in {round(finish - start, 10)} second(s) and used {n_cores=}\n')

'''

    values = list(results)
    print(values)

    combined_List = create_lists_of_two(values)
    # print(combined_List)
    # print(combined_List[0])
    # print(merge_arrays(combined_List[0][0],combined_List[0][1]))
    # print(split_list_array_merge(combined_List[0]))


    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(split_list_array_merge, combined_List)

    # finish = time.perf_counter()

    values = list(results)
    print(len(values))

    # index = 0
    # set_lists = []
    # for _ in range(0, len(values), 2):
    #     set_lists.append([values[index], values[index+(int(len(values)/2))]])
    #     print(index,set_lists)
    #     # print(index, values[index],values[index+(int(len(values)/2))])
    #     index +=1


    # for result in results:
    #     print(result)


    # start = time.perf_counter()
    #
    # sorted_list = merge_sort(unsorted_list)
    #
    # finish = time.perf_counter()
    #
    # print(sorted_list)
    # print(f'Finished in {round(finish-start, 10)} second(s)\n')


    # start = time.perf_counter()
    #
    # merge_sort(randomlist100)
    #
    # finish = time.perf_counter()
    #
    #
    # print(f'Finished in {round(finish-start, 10)} second(s) Single core')
'''