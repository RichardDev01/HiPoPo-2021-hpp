from typing import List
import time
import numpy as np
import concurrent.futures
import matplotlib.pyplot as plt

#Studentnummer
np.random.seed(1762581)


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
    """
    splitting a 2D list of list in to 2 seperate parameters for merge arrays function
    :param mainlist: [[int],[int]]
    :return: Sorted list of ints
    """
    array1 = mainlist[0]
    array2 = mainlist[1]
    return merge_arrays(array1,array2)

def merge_arrays(array1: List[int], array2: List[int]) -> List[int]:
    """https://www.geeksforgeeks.org/python-combining-two-sorted-lists/
    Code van geekforgeeks om merge arrays iteratief temaken
    """
    size_1 = len(array1)
    size_2 = len(array2)

    res = []
    i, j = 0, 0

    while i < size_1 and j < size_2:
        if array1[i] < array2[j]:
            res.append(array1[i])
            i += 1

        else:
            res.append(array2[j])
            j += 1

    res = res + array1[i:] + array2[j:]
    return res


def chunk_slicer(mainlist: List[int], n_chunks:int = 4) -> List[int]:
    """
    Deviding a list in to chunks and returning it in a list format evenly
    :param mainlist: [int] a list of intergers
    :param n_chunks: number of chunks
    :return: a list of intergerlists
    """
    return list(mainlist[i::n_chunks] for i in range(n_chunks))


def merge_lists_of_two(mainlist):
    """
    From a given list of multiple lists, combine them in sets of 2
    :param mainlist: main list of lists
    :return: merged list
    """
    index = 0
    values = mainlist
    set_lists = []
    for _ in range(0, len(values), 2):
        set_lists.append([values[index], values[index+(int(len(values)/2))]])
        index += 1
    return set_lists


def process_join_sort(pre_results):
    """
    Merging the results of the process together and repeat the sorting
    """
    values = list(pre_results)
    # print(values)

    while len(values) >= 2:
        combined_List = merge_lists_of_two(values)

        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = executor.map(split_list_array_merge, combined_List)
        values = list(results)
    return values


def get_time_complex(list_of_sorting_lists: [[int]], n_cores: int) -> {int: float}:
    """
    This function times the proces and returns the time with the length of the list
    :return:
    """
    return_times_dict = {}

    for unsorted_list in list_of_sorting_lists:
        start = time.perf_counter()

        chunks = chunk_slicer(randomlist100, n_cores)
        with concurrent.futures.ProcessPoolExecutor(max_workers= n_cores) as executor:
            results = executor.map(merge_sort, chunks)

        process_join_sort(results)

        finish = time.perf_counter()
        elapsed_time = round(finish - start, 10)

        return_times_dict[len(unsorted_list)] = elapsed_time
    return return_times_dict

if __name__ == '__main__':
    low = 0
    high = 100

    randomlist100 = list(np.random.randint(low=0, high=100, size= 100))
    randomlist250 = list(np.random.randint(low=0, high=100, size= 250))
    randomlist500 = list(np.random.randint(low=0, high=100, size= 500))
    randomlist750 = list(np.random.randint(low=0, high=100, size= 750))
    randomlist1000 = list(np.random.randint(low=0, high=100, size= 1000))
    randomlist1250 = list(np.random.randint(low=0, high=100, size=1250))
    randomlist1500 = list(np.random.randint(low=0, high=100, size=1500))

    unsortedlists = [randomlist100, randomlist250, randomlist500, randomlist750, randomlist1000, randomlist1250,
                     randomlist1500]

    time_complex_data_1c = get_time_complex(unsortedlists, 1)
    time_complex_data_2c = get_time_complex(unsortedlists, 2)
    time_complex_data_4c = get_time_complex(unsortedlists, 4)
    time_complex_data_8c = get_time_complex(unsortedlists, 8)

    print(f"{time_complex_data_1c=} \n {time_complex_data_2c=} \n {time_complex_data_4c=} \n {time_complex_data_8c=}")

    plt.plot(time_complex_data_1c.keys(), time_complex_data_1c.values())
    plt.plot(time_complex_data_2c.keys(), time_complex_data_2c.values())
    plt.plot(time_complex_data_4c.keys(), time_complex_data_4c.values())
    plt.plot(time_complex_data_8c.keys(), time_complex_data_8c.values())

    plt.legend(["1 Core", "2 Cores", "4 Cores", "8 Cores"])
    plt.xlabel('N in list')
    plt.ylabel('time')
    plt.title("comparison")

    plt.show()
