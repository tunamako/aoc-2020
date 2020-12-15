#from aocd.models import Puzzle

import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math


YEAR = 2020
DAY = 15


def play_gaem(array, cap):
    spoken = dict()
    last = 0

    for i, num in enumerate(array):
        spoken[num] = i + 1

    for i in range(len(array) + 1, cap):
        if last in spoken:
            tmp = i - spoken[last]
            spoken[last] = i
            last = tmp
        else:
            spoken[last] = i
            last = 0

    return last

def part_one(_input):
    _input = [int(i) for i in _input.split(',')]
    return play_gaem(_input, 2020)

def part_two(_input):
    _input = [int(i) for i in _input.split(',')]
    return play_gaem(_input, 30000000)


if __name__ == '__main__':
    #_input = "6,19,0,5,7,13,1"
    _input = "0,3,6"
    #_input = open('bigboy').readlines()

    #print(part_one(_input))
    #print(part_two(_input))

    cProfile.run('print(part_one(_input))')
    cProfile.run('print(part_two(_input))')
