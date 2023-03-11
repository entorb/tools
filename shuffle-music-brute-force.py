import itertools as it

# FINDING:
# 10^20 = 1.0e+20 combinations -> no brute force solution possible


def check_how_many_played(playorder: list) -> int:
    """ counts how many songs are played """
    how_many_played = set(playorder)  # set is a unique list
    return len(how_many_played)


amount_of_songs = 10
amount_of_songs_80pct = round(amount_of_songs*0.8, 0)

cnt_80pct_played = 0

for playorder in it.product(range(amount_of_songs), repeat=20):
    if check_how_many_played(playorder) >= amount_of_songs_80pct:
        cnt_80pct_played += 1
        # print(tup)


# # step 1: manually initialize
# all_playorders = []
# for song in range(amount_of_songs):
#     playorder = [song, ]
#     all_playorders.append(playorder)


# def add_playorders(all_playorders: list) -> list:
#     prev_playorders = all_playorders
#     all_playorders = []
#     for prev_playorder in prev_playorders:
#         for song in range(amount_of_songs):
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
# for tup in it.product(range(amount_of_songs), repeat=20):
#     print(tup)
