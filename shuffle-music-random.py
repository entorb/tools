import random
import time
import multiprocessing

# Question
# If a listen to music in shuffle mode, how long do I need to listen until I most probable have heard all / 80% of the songs

# Approach here
# many loops of random playorder

# TODO
# use multiprocessing to speed up
# use pandas and matplotlib zu draw charts


def check_all_played(total_songs: int, playorder: list) -> bool:
    """ 
    checks if all songs are played = in playorder
    returns true if so, else false
    """
    for song in range(total_songs):
        if song not in playorder:
            return False
    return True


assert check_all_played(6, (0, 1, 2, 3, 4, 5)) == True
assert check_all_played(6, (5, 4, 3, 2, 1, 0)) == True
assert check_all_played(6, (0, 1, 2, 3, 4, 0)) == False


def check_how_many_played(playorder: list) -> int:
    """ counts how many songs are played """
    how_many_played = set(playorder)  # set is a unique list
    return len(how_many_played)


assert check_how_many_played((0, 1, 2, 3, 4, 5)) == 6
assert check_how_many_played((0, 0, 2, 2, 4, 5)) == 4


def gen_rand_playorder(total_songs: int, num_songs_played: int) -> list:
    """
    generates a list of random playorder
    """
    playorder = []
    for step in range(num_songs_played):
        playorder.append(random.randint(0, total_songs-1))
    return playorder


def loop_over_rand_playorders(total_songs: int, num_songs_played: int, num_test_loops: int):
    total_songs_80pct = round(total_songs*0.8, 0)
    cnt_all_played = 0
    cnt_80pct_played = 0
    # l_cnt_songs_played = []
    for i in range(num_test_loops):
        playorder = gen_rand_playorder(total_songs, num_songs_played)
        # if check_all_played(total_songs, gen_rand_playorder(total_songs, num_songs_played)):
        if check_all_played(total_songs, playorder):
            cnt_all_played += 1
        if check_how_many_played(playorder) >= total_songs_80pct:
            cnt_80pct_played += 1
    # l_cnt_songs_played.append(check_how_many_played(playorder))
    result = (num_songs_played,
              100.0 * cnt_all_played / num_test_loops,
              100.0 * cnt_80pct_played / num_test_loops)
    return result


if __name__ == '__main__':
    #    freeze_support()

    total_songs = 100
    num_test_loops = 1000
    time_start = time.time()

    # # single processing
    # results = []
    # for num_songs_played in range(total_songs, 4*total_songs+1):
    #     result = loop_over_rand_playorders(
    #         total_songs=total_songs,
    #         num_songs_played=num_songs_played,
    #         num_test_loops=num_test_loops
    #     )
    #     results.append(result)

    # multi processing
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count()-1)
    L1 = []
    for num_songs_played in range(total_songs, 4*total_songs+1):
        L2 = (total_songs, num_songs_played, num_test_loops)
        L1.append(L2)
    results = pool.starmap(loop_over_rand_playorders, L1)
    del L1, L2

    duration = time.time() - time_start
    print("%.1f min" % (duration/60))
    # Laptop, 4 cores:
    # Single: 2.0 min
    # Multi: 1.1 min with 4 processes
    # Multi: 1.1 min with 3 processes
    # Multi: 4.6 min in debug mode with 4 processes

    for result in results:
        num_songs_played, pct_all_played, pct_80pct_played = result
        # print(f"For {total_songs} songs and {num_songs_played} steps\nthe probability to have all played is %.1f%%\nthe probability to have 80%% played is %.1f%%" %
        #       (pct_all_played, pct_80pct_played)
        #       )
