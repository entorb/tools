import itertools as it
import math
import time

# FINDING:
# 10^20 = 1.0e+20 combinations -> no brute force solution possible

# TODO use multiprocessing to speed up


def check_all_played(total_songs: int, playorder: list) -> bool:
    """
    checks if all songs are played = in playorder
    returns true if so, else false
    """
    for song in range(total_songs):
        if song not in playorder:
            return False
    return True


def check_cnt_unique_played(playorder: list) -> int:
    """ counts how many different songs are played """
    cnt_unique_played = set(playorder)  # set is a unique list
    return len(cnt_unique_played)


total_songs = 6
num_songs_played = 10

num_playorder_combinations = int(math.pow(total_songs, num_songs_played))
print(f"{total_songs} total songs and {num_songs_played} songs played give {num_playorder_combinations} combinations")

total_songs_80pct = round(total_songs*0.8, 0)
cnt_all_played = 0
cnt_80pct_played = 0

timestart = time.time()
for playorder in it.product(range(total_songs), repeat=num_songs_played):
    if check_all_played(total_songs=total_songs, playorder=playorder):
        cnt_all_played += 1
    if check_cnt_unique_played(playorder=playorder) >= total_songs_80pct:
        cnt_80pct_played += 1
        # print(tup)
duration = time.time() - timestart
print("%.1f min" % (duration/60))
print("%.1f mill combinations per sec" %
      (num_playorder_combinations/duration / 10 ** 6))

print(f"For {total_songs} songs and {num_songs_played} steps\nthe probability to have all played is %.1f%%\nthe probability to have 80%% played is %.1f%%" %
      (100.0 * cnt_all_played / num_playorder_combinations,
       100.0 * cnt_80pct_played / num_playorder_combinations)
      )

# # step 1: manually initialize
# all_playorders = []
# for song in range(total_songs):
#     playorder = [song, ]
#     all_playorders.append(playorder)


# def add_playorders(all_playorders: list) -> list:
#     prev_playorders = all_playorders
#     all_playorders = []
#     for prev_playorder in prev_playorders:
#         for song in range(total_songs):
#             playorder = list(prev_playorder)  # copy elements, not linking
#             playorder.append(song)
#             all_playorders.append(playorder)
#     return all_playorders


#  for i3 in range(20):
#      for i2 in range(20):
#          for i1 in range(20):
#              l = i1, i2, i3
#              print(l)
#  this becomes:
# for tup in it.product(range(total_songs), repeat=20):
#     print(tup)
