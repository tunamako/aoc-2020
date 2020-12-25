from aocd.models import Puzzle

import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math


YEAR = 2020
DAY = 24

DELTAS = {
    'n': (0, -2), 'ne': (1, -1), 'nw': (-1, -1),
    'e': (2, 0),
    's': (0, 2), 'se': (1, 1), 'sw': (-1, 1),
    'w': (-2, 0),
}

def reduce_tilestring(string):
    loc = [0, 0]
    i = 0
    while i < len(string):
        try:
            _dir = string[i:i+2]
            if _dir not in DELTAS:
                _dir = string[i]
        except:
            _dir = string[i]

        d = DELTAS[_dir]
        loc[0] += d[0]
        loc[1] += d[1]
        i += len(_dir)

    return tuple(loc)

def part_one(_input):
    tiles = Counter([reduce_tilestring(t.strip('\n')) for t in _input])
    return sum([t % 2 == 1 for t in tiles.values()])

def get_neighbors(loc):
    ret = set()
    for d in ["e","ne","nw","w","se","sw"]:
        ret.add((loc[0]+DELTAS[d][0], loc[1]+DELTAS[d][1]))
    return ret

def get_black_neighbors(loc, tiles):
    count = 0
    for n in get_neighbors(loc):
        if n in tiles:
            count += int(tiles[n])
    return count

def part_two(_input):
    tiles = defaultdict(bool)

    for line in _input:
        loc = reduce_tilestring(line.strip('\n'))
        tiles[loc] = not tiles[loc]

    for day in range(1, 101):
        to_flip = set()
        to_add = set()
        for t in tiles:
            for n in get_neighbors(t):
                if n not in tiles:
                    to_add.add(n)

        for t in to_add:
            tiles[t]

        for t, state in tiles.items():
            neighbors = get_black_neighbors(t, tiles)

            if state and (neighbors == 0 or neighbors > 2):
                to_flip.add(t)
            elif (not state) and neighbors == 2:
                to_flip.add(t)

        for t in to_flip:
            tiles[t] = not tiles[t]

    return sum(tiles.values())

if __name__ == '__main__':
    puzzle = Puzzle(year=YEAR, day=DAY)
    _input = puzzle.input_data.split('\n')
    #_input = open('input').readlines()

    print(part_one(_input))
    print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
