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
    rowmax = 127
    rowmin = 0
    colmax = 7
    colmin = 0

    for c in line[:-3]:
        if c == 'F':
            rowmax = rowmin + ((rowmax - rowmin) // 2)
        elif c == 'B':
            rowmin = rowmin + ((rowmax - rowmin) // 2) + 1

    row = rowmin
    for c in line[-3:]:
        if c == 'L':
            colmax = colmin + ((colmax - colmin) // 2)
        elif c == 'R':
            colmin = colmin + ((colmax - colmin) // 2) + 1
    col = colmin

    return row, col

def get_id(row, col):
    return (row * 8) + col

def part_one(_input):
    max_id = 0
    for line in _input:
        max_id = max(get_id(*get_pos(line)), max_id)

    return max_id

def part_two(_input):
    ids = {line: get_pos(line) for line in _input}
    print(ids)
    for i in ids:
        for j in ids:
            if (get_id(*ids[i]) - get_id(*ids[j]) == 2) and (ids[j][0] not in [127, 0]) and (ids[i][0] not in [127, 0]):
                targetid = get_id(*ids[i])

    return targetid - 1


if __name__ == '__main__':
    puzzle = Puzzle(year=YEAR, day=DAY)
    _input = puzzle.input_data.split('\n')
    #_input = open('bigboy').readlines()

    #print(part_one(_input))
    print(part_two(_input))
    #print(get_id("FBFBBFFRLR"))
    #submit(part_one(_input), part="a", day=DAY, year=YEAR)
    #submit(part_two(_input), part="b", day=DAY, year=YEAR)

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
