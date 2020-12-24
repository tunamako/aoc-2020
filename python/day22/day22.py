from aocd.models import Puzzle

import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math


YEAR = 2020
DAY = 22


def part_one(_input):
    p1 = [int(c) for c in _input[0].split(':')[1].strip('\n').split('\n')[::-1]]
    p2 = [int(c) for c in _input[1].split(':')[1].strip('\n').split('\n')[::-1]]

    while p1 and p2:
        c1, c2 = p1.pop(), p2.pop()
        if c1 > c2:
            p1 = [c2, c1] + p1
        else:
            p2 = [c1, c2] + p2

    winner = p1 if p1 else p2

    score = 0
    for i, c in enumerate(winner):
        score += (i+1) * c

    return score

def score(winner):
    return sum([(i+1)*c for i, c in enumerate(winner)])

def combat(p1, p2):
    seen = set()

    while p1 and p2:
        state_hash = (tuple(p1), tuple(p2))
        if state_hash in seen:
            return p1, p2

        seen.add(state_hash)
        c1, c2 = p1.pop(), p2.pop()

        if len(p1) >= c1 and len(p2) >= c2:
            sub_p1, sub_p2 = combat(p1[-1*c1:], p2[-1*c2:])
            if sub_p1:
                p1 = [c2, c1] + p1
            else:
                p2 = [c1, c2] + p2
        else:
            if c1 > c2:
                p1 = [c2, c1] + p1
            else:
                p2 = [c1, c2] + p2

    return p1, p2


def part_two(_input):
    p1 = [int(c) for c in _input[0].split(':')[1].strip('\n').split('\n')[::-1]]
    p2 = [int(c) for c in _input[1].split(':')[1].strip('\n').split('\n')[::-1]]

    p1, p2 = combat(p1, p2)
    return score(p1 if p1 else p2)


if __name__ == '__main__':
    puzzle = Puzzle(year=YEAR, day=DAY)
    _input = puzzle.input_data.split('\n\n')
    #_input = open('input').read().split('\n\n')

    print(part_one(_input))
    print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
