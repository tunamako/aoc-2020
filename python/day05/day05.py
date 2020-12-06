from aocd import submit
from aocd.models import Puzzle

import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math

YEAR = 2020
DAY = 5


def get_pos(line):
    line = line.translate(line.maketrans("FBLR", "0101"))

    return int(line[:-3], 2), int(line[-3:], 2)


def get_id(line):
    row, col = get_pos(line)

    return (row * 8) + col


def part_one(_input):
    return max([get_id(line) for line in _input])


def part_two(_input):
    seat_positions = {get_id(line): get_pos(line) for line in _input}
    ids = sorted(list(seat_positions))

    for i in range(len(ids)):
        if (ids[i+1] - ids[i] == 2):
            seat_ahead = seat_positions[ids[i]]
            seat_behind = seat_positions[ids[i + 1]]

            if seat_ahead[0] not in (0, 127) and seat_behind[0] not in (0, 127):
                return ids[i] + 1


if __name__ == '__main__':
    puzzle = Puzzle(year=YEAR, day=DAY)
    _input = puzzle.input_data.split('\n')
    #_input = open('bigboy').readlines()

    print(part_one(_input))
    print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
