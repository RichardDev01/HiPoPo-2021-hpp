# Computes an approximation of Pi by summing up
# a series of terms.  The more terms, the closer
# the approximation.
# Based on a variation of the Gregory-Leibniz series approximation
#
import threading
import concurrent.futures
from timeit import default_timer as timer


def f(x):
    """
    The function being integrated, and which returns
    an approximation of Pi when summed up over an interval
    of integers.
    """
    return 4.0 / (1 + x * x)


class WorkerThread(threading.Thread):

    def __init__(self, args):
        """
        args must contain n1, n2, and deltaX, in that order.
        """
        threading.Thread.__init__(self, args=args)
        self.n2 = args[0]  # Sum
        self.deltaX = args[1]
        self._lock = threading.Lock()

    def run(self, i):
        """
        This will be called automatically by start() in
        main.  It's the method that does all the work.
        """
        # self._lock.acquire()
        self.n2 += f(i * self.deltaX)
        # self._lock.release()

    def get(self):
        """
        gets the computed sum.
        """
        return self.n2 * self.deltaX


class WorkerThreadRework(threading.Thread):

    def __init__(self, args):
        """
        args must contain n1, n2, and deltaX, in that order.
        """
        threading.Thread.__init__(self, args=args)
        self.n1 = args[0]  # N
        self.n2 = args[1]  # Sum
        self.deltaX = args[2]

    def run(self):
        """
        This will be called automatically by start() in
        main.  It's the method that does all the work.
        """

        start = timer()
        threads = list()
        for index in range(self.n1):
            x = threading.Thread(target=self.compute_function, args=(index,))
            threads.append(x)
            x.start()

        for x in threads:
            x.join()

        # display results

        elapsed_time = timer() - start

        print(f"Threading attempt #2\n sum = {self.get()} \n elapsed_time time {elapsed_time}\n")

    def compute_function(self, index):
        self.n2 += f(index * self.deltaX)

    def get(self):
        """
        gets the computed sum.
        """
        return self.n2 * self.deltaX

def main():
    """
    Gets a number of terms from the user, then sums
    up the series and prints the resulting sum, which
    should approximate Pi.
    """

    # get the number of terms
    # N = int(input("> "))
    N = 10000

    sum = 0.0  # where we sum up the individual
    # intervals
    deltaX = 1.0 / N  # the interval

    # ------------------------------------------------------------
    start = timer()
    workers = WorkerThread(args=[sum, deltaX])

    with concurrent.futures.ThreadPoolExecutor(max_workers=N) as executor:
        for i in range(N):
            executor.submit(workers.run(i))

    elapsed_time = timer() - start
    print(f"Threading attempt #1\n sum = {workers.get()} \n elapsed_time time {elapsed_time}\n")

    # ------------------------------------------------------------

    workersRework = WorkerThreadRework(args=[N, sum, deltaX])

    workersRework.start()

    # ------------------------------------------------------------


    start = timer()
    # sum over N terms
    for i in range(N):
        sum += f(i * deltaX)

    elapsed_time = timer() - start
    print(f"No threading \n sum = {(sum * deltaX)}\n elapsed_time time {elapsed_time}\n")


main()
