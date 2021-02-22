# Computes an approximation of Pi by summing up
# a series of terms.  The more terms, the closer
# the approximation.
# Based on a variation of the Gregory-Leibniz series approximation
#
import threading


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
        self.n1 = args[0]  # Total N
        self.n2 = args[1]  # Total Workers
        self.deltaX = args[2]
        self.value = 0

    def run(self):
        """
        This will be called automatically by start() in
        main.  It's the method that does all the work.
        """
        # Itereer over je batch en verzamel de som bij elkaar net zoals de single threaded versie ( < 5 regels code)
        N = round(self.n1 / self.n2)
        self.n1 -= N

        for i in range(N):
            self.value += f(i * self.deltaX)
        pass

    def get(self):
        """
        gets the computed sum.
        """
        pass


def main():
    """
    Gets a number of terms from the user, then sums
    up the series and prints the resulting sum, which
    should approximate Pi.
    """

    # get the number of terms
    N = 10000

    sum = 0.0  # where we sum up the individual
    # intervals
    deltaX = 1.0 / N  # the interval

    # sum over N terms wordt nu:
    # itereer over N terms in batches van batch_size
    # maak een worker aan met de respectievelijke batch en laat die summen over N terms (dus in de worker)
    # start je worker
    # voeg toe aan een lijst van workers
    # < 10 regels code

    threadCount = 10

    batchSize = N / threadCount

    workers = WorkerThread(args=[sum, threadCount, deltaX])

    threads = list()
    for i in range(N, batchSize):
        x = threading.Thread(target=workers.run(), args=(i,))
        threads.append(x)
        x.start()

    for x in threads:
        x.join()

    # Itereer over je workers en zorg dat alle data bij elkaar komt. (< 5 regels code)
    pass

    # display results
    print("sum = %1.9f" % (sum * deltaX))


main()
