from aocd.models import Puzzle

import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math


YEAR = 2020
DAY = 14


def apply_mask(mask, value):
    value = "{0:b}".format(value)
    value = list(value.zfill(len(mask)))

    for i in range(len(mask)):
        if mask[i] != 'X':
            value[i] = mask[i]

    value = ''.join(value)
    return int(value, base=2)

def part_one(_input):
    memory = defaultdict(lambda: 0)
    mask = ""

    for line in _input:

        if "mask" in line:
            mask = line.split(' ')[2]
        elif "mem" in line:
            adr = int(line[4:line.index(']')])

            memory[adr] = apply_mask(mask, int(line.split(' ')[2]))

    return sum(memory.values())


def apply_mask2(mask, value):
    value = "{0:b}".format(value)
    value = list(value.zfill(len(mask)))
    value_start = value.index('1')

    for i in range(len(mask)):
        if mask[i] != '0':
            value[i] = mask[i]

    return ''.join(value)


def part_two(_input):
    memory = defaultdict(lambda: 0)
    mask = ""

    for line in _input:

        if "mask" in line:
            mask = line.split(' ')[2]
        elif "mem" in line:
            value = int(line.split(' ')[2])
            adr_space = apply_mask2(mask, int(line[4:line.index(']')]))
            X_indices = [i for i, ltr in enumerate(adr_space) if ltr == 'X']

            adr_space = adr_space.replace('X', '0')
            
            combs = []
            for i in range(len(X_indices) + 1):
                combs += list(combinations(X_indices, i))

            for comb in combs:
                new_adr = list(adr_space)
                for i in comb:
                    new_adr[i] = '1'

                new_adr = int(''.join(new_adr), base=2)
                memory[new_adr] = value

    return sum(memory.values())


if __name__ == '__main__':
    puzzle = Puzzle(year=YEAR, day=DAY)
    _input = puzzle.input_data.split('\n')
    #_input = [line[:-1] for line in open('input').readlines()]

    print(part_one(_input))
    print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
