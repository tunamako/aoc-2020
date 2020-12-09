from aocd.models import Puzzle

import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math

YEAR = 2020
DAY = 9


def part_one(_input):
    predicate = _input[:25]

    for num in _input[25:]:
        if num not in set(map(sum, combinations(predicate, 2))):
            return num

        predicate = predicate[1:] + [num]


def part_two(_input):
    invalid = part_one(_input)

    for i in range(len(_input)):
        acc = 0
        for j in range(i, len(_input)):
            acc += _input[j]

            if acc == invalid:
                return max(_input[i:j+1]) + min(_input[i:j+1])


if __name__ == '__main__':
    puzzle = Puzzle(year=YEAR, day=DAY)
    _input = list(map(int, puzzle.input_data.split('\n')))
    #_input = open('bigboy').readlines()

    print(part_one(_input))
    print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
