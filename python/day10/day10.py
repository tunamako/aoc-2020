from aocd.models import Puzzle

import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math


YEAR = 2020
DAY = 10


test1 = set([
    16,
    10,
    15,
    5,
    1,
    11,
    7,
    19,
    6,
    12,
    4,
])


test2 = set([
    28,
    33,
    18,
    42,
    31,
    14,
    46,
    20,
    48,
    47,
    24,
    23,
    49,
    45,
    19,
    38,
    39,
    11,
    1,
    32,
    25,
    35,
    8,
    17,
    7,
    9,
    4,
    2,
    34,
    10,
    3,
])


def find_chain(adapters, chain=None, cur_joltage=0):
    if chain is None: chain = []

    if not adapters:
        return chain

    for i, a in enumerate(adapters):

        if a - 3 <= cur_joltage <= a + 1:
            adapters.remove(a)

            out = find_chain(adapters, chain + [a], a) 
            if out is None:
                adapters.add(a)
            else:
                return out

    return None


def part_one(adapters):
    adapters = adapters.copy()
    rating =  max(adapters) + 3

    chain = find_chain(adapters)

    onediffs = 0
    threediffs = 1

    if chain[0] == 1:
        onediffs += 1
    elif chain[0] == 3:
        threediffs += 1

    for i in range(len(chain) - 1):
        if abs(chain[i + 1] - chain[i]) == 1:
            onediffs += 1
        elif abs(chain[i + 1] - chain[i]) == 3:
            threediffs += 1

    return onediffs * threediffs


def part_two(adapters):
    adapters = sorted(list(adapters))

    step_counts = dict()
    step_counts[0] = 1

    for a in adapters:
        step_counts[a] = 0
        if a - 3 in step_counts:
            step_counts[a] += step_counts[a - 3]
        if a - 2 in step_counts:
            step_counts[a] += step_counts[a - 2]
        if a - 1 in step_counts:
            step_counts[a] += step_counts[a - 1]

    return(step_counts[max(adapters)])

if __name__ == '__main__':
    puzzle = Puzzle(year=YEAR, day=DAY)
    _input = set(map(int, puzzle.input_data.split('\n')))
    #_input = open('bigboy').readlines()

    print(part_one(_input))
    print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
