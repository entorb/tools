import threading
import queue
import os
import time


def worker(q_work: queue.Queue, results: dict):
    while not q_work.empty():
        i, s = q_work.get()
        time.sleep(.1)
        result = (i, s, os.getpid())
        results[i] = result
        q_work.task_done()


if __name__ == '__main__':
    d_results = {}  # threads can write into dict
    # gen. pile of work
    l_pile_of_work = []
    for i in range(1_000):
        tup = (i, "n"+str(i))
        l_pile_of_work.append((tup))
    # convert list of work to queue
    q_pile_of_work = queue.Queue(
        maxsize=len(l_pile_of_work))  # maxsize=0 -> unlimited
    for params in l_pile_of_work:
        q_pile_of_work.put(params)
    # gen threads
    num_threads = 100
    l_threads = []  # List of threads, not used here
    for i in range(num_threads):
        t = threading.Thread(name='myThread-'+str(i),
                             target=worker,
                             args=(q_pile_of_work, d_results),
                             daemon=True)
        l_threads.append(t)
        t.start()
    q_pile_of_work.join()  # wait for all threas to complete
    l_results_unsorted = d_results.values()
    l_results = sorted(l_results_unsorted)  # sort by i
