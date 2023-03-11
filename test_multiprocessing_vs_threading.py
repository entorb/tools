#!/usr/bin/env python3
"""
Comparing multiprocessing and threading.
"""
import math
import multiprocessing
import os
import queue
import threading
import time


def worker_core(i: int, s: str) -> list:
    """
    For worker_core_cpu and worker_core_io.
    """
    result = i, s, os.getpid()
    time.sleep(0.1)
    return result


def worker_core_cpu(i: int, s: str) -> list:
    """
    For all CPU limited worker implementations.
    """
    my_sum = 0
    for j in range(1_000):
        my_sum += math.sqrt(i + j)
    result = worker_core(i=i, s=s)
    return result


def worker_core_io(i: int, s: str) -> list:
    """
    For all I/O limited worker implementations.
    """
    time.sleep(0.1)
    result = worker_core(i=i, s=s)
    return result


def worker_multiprocessing_1(i: int, s: str) -> list:
    return worker_core_cpu(i=i, s=s)


def worker_multiprocessing_2(
    q_work: multiprocessing.Queue,
    q_results: multiprocessing.Queue,
):
    """
    Not faster than multiprocessing_1.
    """
    while not q_work.empty():
        i, s = q_work.get()
        result = worker_core_cpu(i=i, s=s)
        q_results.put(result)


def worker_threading_1(q_work: queue.Queue, results: dict):
    """For threading_1."""
    while not q_work.empty():
        i, s = q_work.get()
        result = worker_core_io(i=i, s=s)
        results[i] = result
        q_work.task_done()


def multiprocessing_1(l_pile_of_work: list):
    """
    For CPU limited tasks.
    """
    num_processes = min(multiprocessing.cpu_count() - 1, len(l_pile_of_work))
    pool = multiprocessing.Pool(processes=num_processes)
    # use map for 1 argument, use starmap for multiple arguments for worker function
    # here each item in l_pile_of_work is a list of 3 elements -> starmap
    l_results_unsorted = pool.starmap(
        func=worker_multiprocessing_1,
        iterable=l_pile_of_work,
    )
    l_results = sorted(l_results_unsorted)  # sort by id
    return l_results


def multiprocessing_2(l_pile_of_work: list):
    """
    For CPU limited tasks.

    not using not re-creation of processes, but fixed number instead
    result: slower than multiprocessing_1
    """
    q_pile_of_work = multiprocessing.Queue(maxsize=len(l_pile_of_work))
    q_results = multiprocessing.Queue(maxsize=len(l_pile_of_work))

    for params in l_pile_of_work:
        q_pile_of_work.put(params)
    del params

    num_processes = min(multiprocessing.cpu_count() - 1, len(l_pile_of_work))
    l_processes = []
    for i in range(num_processes):
        p = multiprocessing.Process(
            name="myProcess-" + str(i),
            target=worker_multiprocessing_2,
            args=(q_pile_of_work, q_results),
            daemon=True,
        )
        l_processes.append(p)
    del i
    for p in l_processes:
        p.start()
    print("started")

    while not q_results.full():
        time.sleep(0.1)
    for p in l_processes:
        p.terminate()
        p.join()
        p.close()
    print("closed")
    del p

    l_results_unsorted = []
    while not q_results.empty():
        result = q_results.get()
        l_results_unsorted.append(result)
    l_results = sorted(l_results_unsorted)  # sort by id
    return l_results


def threading_1(l_pile_of_work: list, num_threads: int):
    """
    For I/O limited tasks.
    """
    q_pile_of_work = queue.Queue(
        maxsize=len(l_pile_of_work),
    )  # maxsize=0 -> unlimited
    for params in l_pile_of_work:
        q_pile_of_work.put(params)
    d_results = {}  # threads can write into dict

    l_threads = []  # List of threads, not used here
    for i in range(num_threads):
        t = threading.Thread(
            name="myThread-" + str(i),
            target=worker_threading_1,
            args=(q_pile_of_work, d_results),
            daemon=True,
        )
        l_threads.append(t)
        t.start()
    q_pile_of_work.join()  # wait for all threas to complete
    l_results_unsorted = d_results.values()
    l_results = sorted(l_results_unsorted)  # sort by id
    return l_results


if __name__ == "__main__":
    l_pile_of_work = []
    loops = 1_000
    for i in range(loops):
        # use index as first parameter
        L2 = (i, "n" + str(i))
        l_pile_of_work.append(L2)
    del L2, i
    time_start = time.time()
    # results = multiprocessing_1(l_pile_of_work)
    # # or
    # results = multiprocessing_2(l_pile_of_work)
    # # or
    results = threading_1(l_pile_of_work, num_threads=100)
    duration = time.time() - time_start
    print("%d sec = %.1f min" % (duration, duration / 60))

    # for res in results:
    #     print('task %d, name %s was done in process %d' % (res))
    # print(len(results))


# multiprocessing_1
# 16 sec = 0.3 min
# multiprocessing_2
#
