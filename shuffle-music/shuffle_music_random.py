#!/usr/bin/env python3
"""
Question: Listening to music in shuffle mode...

how long do I need to listen until I most probable have heard all / 80% of the songs?

Approach here
many loops of random playorder

Mathematical solution might be found here
https://en.m.wikipedia.org/wiki/Negative_binomial_distribution
"""
import multiprocessing
import random
import time

import matplotlib.pyplot as plt
import pandas as pd
import shuffle_music_lib

# TODO
# generated random data -> file and re-generate only when not existing to speepup the plotting

# DONE
# use multiprocessing to speed up
# use pandas and matplotlib zu draw charts


def gen_rand_playorder(total_songs: int, num_songs_played: int) -> tuple[int]:
    """
    Generate a list of random playorder.
    """
    playorder: list[int] = []
    for _step in range(num_songs_played):
        playorder.append(random.randint(0, total_songs - 1))  # noqa: S311
    return tuple(playorder)


def loop_over_rand_playorders(
    total_songs: int,
    num_songs_played: int,
    num_test_loops: int,
) -> tuple[int, float, float]:
    total_songs_80pct = round(total_songs * 0.8, 0)
    cnt_all_played = 0
    cnt_80pct_played = 0
    # l_cnt_songs_played = []
    for _i in range(num_test_loops):
        playorder = gen_rand_playorder(total_songs, num_songs_played)
        cnt_unique_played = shuffle_music_lib.check_cnt_unique_played(
            playorder,
        )
        if cnt_unique_played >= total_songs_80pct:
            cnt_80pct_played += 1
        if cnt_unique_played == total_songs:
            cnt_all_played += 1
        # if shuffle_music_lib.check_all_played(total_songs, playorder):
        #     cnt_all_played += 1

    # l_cnt_songs_played.append(check_cnt_unique_played(playorder))
    result = (
        num_songs_played,
        100.0 * cnt_all_played / num_test_loops,
        100.0 * cnt_80pct_played / num_test_loops,
    )
    return result


def plot_results(
    total_songs: int, num_test_loops: int, results: tuple[int, float, float]
) -> None:
    df = pd.DataFrame(
        data=results,
        columns=(
            "num_songs_played",
            "pct_all_played",
            "pct_80pct_played",
        ),
    )
    df.set_index(["num_songs_played"], inplace=True)
    # print(df.head())

    fig, axes = plt.subplots(figsize=(8.00, 6.00))  # 10.80/2, 19.20/2
    df["pct_80pct_played"].plot(linewidth=2.0, legend=True, zorder=1)
    df["pct_all_played"].plot(linewidth=2.0, legend=True, zorder=2)
    plt.grid(axis="both")
    axes.set_axisbelow(True)  # for grid below the lines
    axes.set_ylim(0, 100)
    import matplotlib.ticker as mtick

    axes.yaxis.set_major_formatter(mtick.PercentFormatter())
    plt.legend(["prob. 80% played", "prob. all played"])
    plt.title(
        f"Shuffling {total_songs} Songs\n(simulation of {num_test_loops} randomized loops)",
    )
    plt.xlabel("Songs Played", fontsize=12)
    plt.ylabel("\nProbability", fontsize=12, labelpad=-5)
    plt.tight_layout()
    plt.savefig(
        fname="shuffle-music/shuffle_music_random-%03d.png" % total_songs,
        format="png",
    )


def run_simulation_single_processing(
    total_songs: int, num_test_loops: int
) -> tuple[tuple[int, float, float]]:
    results: list[tuple[int, float, float]] = []
    for num_songs_played in range(total_songs, 5 * total_songs + 1):
        result = loop_over_rand_playorders(
            total_songs=total_songs,
            num_songs_played=num_songs_played,
            num_test_loops=num_test_loops,
        )
        results.append(result)
    return tuple(results)


def run_simulation_multi_processing(total_songs: int, num_test_loops: int) -> list:
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count() - 1)
    l_pile_of_work = []
    for num_songs_played in range(int(total_songs * 0.8), int(5 * total_songs + 1)):
        l_pile_of_work.append((total_songs, num_songs_played, num_test_loops))
    # del num_songs_played
    results = pool.starmap(
        func=loop_over_rand_playorders,
        iterable=l_pile_of_work,
    )
    return results


if __name__ == "__main__":
    total_songs = 6
    num_test_loops = 10_000

    results: list = []

    time_start = time.time()
    # results = run_simulation_single_processing(
    #     total_songs=total_songs, num_test_loops=num_test_loops)
    results = run_simulation_multi_processing(
        total_songs=total_songs,
        num_test_loops=num_test_loops,
    )

    duration = time.time() - time_start
    print("%d sec = %.1f min" % (duration, duration / 60))
    # Desktop 12 cores
    # for
    # total_songs = 100
    # num_test_loops = 10000
    # 93 sec = 1.6 min

    plot_results(
        total_songs=total_songs,
        num_test_loops=num_test_loops,
        results=results,
    )

    # for result in results:
    #     num_songs_played, pct_all_played, pct_80pct_played = result
    # print(f"For {total_songs} songs and {num_songs_played} steps\nthe probability to have all played is %.1f%%\nthe probability to have 80%% played is %.1f%%" %
    #       (pct_all_played, pct_80pct_played)
    #       )
