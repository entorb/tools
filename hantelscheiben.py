import sys
import itertools

hanteln = (20, 10, 5, 2, 2, 2.5, 1.5)


# all combinations via Cartesian product
hanteln = sorted(hanteln, reverse=True)
l = list(zip(hanteln, [0] * len(hanteln)))
combinations_all = []
for combination in itertools.product(*l):
    combinations_all.append(combination)
del l, combination
del itertools

# reduce to unique combinations, prefering the ones with least hantelns
combinations_unique = {}
for combination in combinations_all:
    # convert tuple to list
    combination = list(combination)
    # remove 0 values
    while 0 in combination:
        combination.remove(0)
    combination = tuple(combination)

    s = sum(combination)
    # add if new sum
    if s not in combinations_unique:
        combinations_unique[s] = combination
    else:
        # overwrite only if length (=count of handeln) is smaller
        if len(combination) < len(combinations_unique[s]):
            combinations_unique[s] = combination
del combinations_all, s, combination

# remove argv[0] = py file
targets = list(sys.argv[1:])
for target in targets:
    target = float(target)

    # find closest combinations
    match_lower = (0, ())
    match_higher = (10000000, ())
    for s in combinations_unique.keys():
        if s <= target and s > match_lower[0]:
            match_lower = (s, combinations_unique[s])
        elif s > target and s < match_higher[0]:
            match_higher = (s, combinations_unique[s])
    del s

    deltaLow = 10000000
    deltaHigh = 10000000
    # print("%.1f : target" % target)
    if match_lower[0] > 0:
        # print("%.1f : %+.1f" %
        #       (match_lower[0], match_lower[0]-target)
        #       + f" via {match_lower[1]}")
        deltaLow = target - match_lower[0]
    if match_higher[0] < 10000000:
        # print("%.1f : %+.1f" %
        #       (match_higher[0], match_higher[0]-target)
        #       + f" via {match_higher[1]}")
        deltaHigh = match_higher[0]-target
#    if deltaLow < deltaHigh:
    print("%.1f -> %.1f" %
            (target, match_lower[0])
              + f" via {match_lower[1]}")
    deltaLow = target - match_lower[0]
#    else:
    print("%.1f -> %.1f" %
              (target, match_higher[0])
              + f" via {match_higher[1]}")
    deltaHigh = match_higher[0]-target
