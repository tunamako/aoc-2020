from aocd import submit
from aocd.models import Puzzle

import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math

YEAR = 2020
DAY = 6


def get_groups(_input):
    return [map(set, g.split('\n')) for g in _input]


def part_one(_input):
    return sum(len(set.union(*g)) for g in get_groups(_input))


def part_two(_input):
    return sum(len(set.intersection(*g)) for g in get_groups(_input))


if __name__ == '__main__':
    puzzle = Puzzle(year=YEAR, day=DAY)
    _input = puzzle.input_data.split('\n\n')
    #_input = open('bigboy').readlines()

    print(part_one(_input))
    print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
