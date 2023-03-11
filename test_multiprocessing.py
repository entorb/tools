#!/usr/bin/env python3
"""
Trying out multiprocessing.
"""
import multiprocessing
import os


def worker(i: int, s: str) -> tuple[int, str, int]:
    result = (i, s, os.getpid())
    return result


if __name__ == "__main__":
    # gen. pile of work
    l_pile_of_work: list[tuple[int, str]] = []
    for i in range(1_000):
        tup = (i, "n" + str(i))
        l_pile_of_work.append(tup)
    # gen pool of processes
    num_processes = min(multiprocessing.cpu_count() - 1, len(l_pile_of_work))
    pool = multiprocessing.Pool(processes=num_processes)
    # start processes on pile of work
    l_results_unsorted = pool.starmap(
        func=worker,
        iterable=l_pile_of_work,  # each item is a list of 2 parrameters
    )
    l_results = sorted(l_results_unsorted)  # sort by i
