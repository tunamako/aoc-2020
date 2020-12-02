from aocd import submit
from aocd.models import Puzzle

import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math


YEAR = 2020
DAY = 2

def fmt_line(line):
    nums, char, paswd = line.split(' ')
    num_one, num_two = nums.split('-')

    return int(num_one), int(num_two), char[0], paswd

def part_one(_input):
    valid = 0
    for line in _input:
        _min, _max, char, paswd = fmt_line(line)

        if _min <= paswd.count(char) <= _max:
            valid += 1

    return valid

def part_two(_input):
    valid = 0
    for line in _input:
        posX, posY, char, paswd = fmt_line(line)

        if (paswd[posX - 1] == char) ^ (paswd[posY - 1] == char):
            valid += 1

    return valid

if __name__ == '__main__':
    puzzle = Puzzle(year=YEAR, day=DAY)
    _input = puzzle.input_data.split('\n')
    #_input = open('bigboy').readlines()

    print(part_one(_input))
    print(part_two(_input))

    #submit(part_one(_input), part="a", day=DAY, year=YEAR)
    #submit(part_two(_input), part="b", day=DAY, year=YEAR)

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
