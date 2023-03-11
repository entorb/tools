import random

# Question
# If a listen to music in shuffle mode, how long do I need to listen until I most probable have heard all / 80% of the songs

# Approach here
# many loops of random playorder

# TODO
# use pandas and matplotlib zu draw charts


def check_all_played(amount_of_songs: int, playorder: list) -> bool:
    """ 
    checks if all songs are played = in playorder
    returns true if so, else false
    """
    for song in range(amount_of_songs):
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


def gen_rand_playorder(amount_of_songs: int, num_steps: int) -> list:
    """
    generates a list of random playorder
    """
    playorder = []
    for step in range(num_steps):
        playorder.append(random.randint(0, amount_of_songs-1))
    return playorder


amount_of_songs = 20
amount_of_songs_80pct = round(amount_of_songs*0.8, 0)
test_loops = 1000
# num_steps = 6
for num_steps in range(amount_of_songs, 4*amount_of_songs+1):
    cnt_all_played = 0
    cnt_80pct_played = 0
    # l_cnt_songs_played = []
    for i in range(test_loops):
        playlist = gen_rand_playorder(amount_of_songs, num_steps)
        # if check_all_played(amount_of_songs, gen_rand_playorder(amount_of_songs, num_steps)):
        if check_all_played(amount_of_songs, playlist):
            cnt_all_played += 1
        if check_how_many_played(playlist) >= amount_of_songs_80pct:
            cnt_80pct_played += 1
        # l_cnt_songs_played.append(check_how_many_played(playlist))
    print(f"For {amount_of_songs} songs and {num_steps} steps\nthe probability to have all played is %.1f%%\nthe probability to have 80%% played is %.1f%%" %
          (100.0 * cnt_all_played / test_loops,
           100.0 * cnt_80pct_played / test_loops)
          )
