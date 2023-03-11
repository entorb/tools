
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


def check_cnt_unique_played(playorder: list) -> int:
    """ counts how many songs are played """
    how_many_played = set(playorder)  # set is a unique list
    return len(how_many_played)


assert check_cnt_unique_played((0, 1, 2, 3, 4, 5)) == 6
assert check_cnt_unique_played((0, 0, 2, 2, 4, 5)) == 4
