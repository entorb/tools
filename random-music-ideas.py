
# step 1: manually initialize
all_playorders = []
for song in range(amount_of_songs):
    playorder = [song, ]
    all_playorders.append(playorder)


def add_playorders(all_playorders: list) -> list:
    prev_playorders = all_playorders
    all_playorders = []
    for prev_playorder in prev_playorders:
        for song in range(amount_of_songs):
            playorder = list(prev_playorder)  # copy elements, not linking
            playorder.append(song)
            all_playorders.append(playorder)
    return all_playorders


#  for i3 in range(20):
#      for i2 in range(20):
#          for i1 in range(20):
#              l = i1, i2, i3
#              print(l)
#  this becomes:
#  for tup in it.product(range(20), repeat=3):
#     print(tup)


def loop_all_playorders(num_plays):
    """
    TODO: could not find a way to dynamically loop over an unknown number of iteration variables
    """
    playorder = list()
    indices = [0] * num_plays  # gen list of 0 filled indices
    for i in range(num_plays):
        playorder = indices
        print(playorder)
