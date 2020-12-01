from aocd import submit
from aocd.models import Puzzle

import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math


YEAR = 2020
DAY = 1


def part_one(_input):
    for i in _input:
        if (j := 2020 - i) in _input:
            return i * j

def part_two(_input):
    for i in _input:
        for j in _input:
            if (k := 2020 - i - j) in _input:
                return i * j * k


if __name__ == '__main__':
    puzzle = Puzzle(year=YEAR, day=DAY)
    _input = set([int(line) for line in puzzle.input_data.split('\n')])
    #_input = open('bigboy').readlines()

    print(part_one(_input))
    print(part_two(_input))

    #submit(part_one(_input), part="a", day=DAY, year=YEAR)
    #submit(part_two(_input), part="b", day=DAY, year=YEAR)
    
    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
