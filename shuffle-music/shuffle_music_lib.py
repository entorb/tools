#!/usr/bin/env python3
"""
Shared methods.
"""


def check_all_played(total_songs: int, playorder: list) -> bool:
    """
    Check if all songs are played = in playorder.

    returns true if so, else false
    """
    # for song in range(total_songs):
    #     if song not in playorder:
    #         return False
    # return True
    return all(not song not in playorder for song in range(total_songs))


assert check_all_played(6, (0, 1, 2, 3, 4, 5)) is True
assert check_all_played(6, (5, 4, 3, 2, 1, 0)) is True
assert check_all_played(6, (0, 1, 2, 3, 4, 0)) is False


def check_cnt_unique_played(playorder: list) -> int:
    """Count how many songs are played."""
    how_many_played = set(playorder)  # set is a unique list
    return len(how_many_played)


assert check_cnt_unique_played((0, 1, 2, 3, 4, 5)) == 6
assert check_cnt_unique_played((0, 0, 2, 2, 4, 5)) == 4
