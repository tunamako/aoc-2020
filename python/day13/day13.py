from aocd.models import Puzzle

import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
from functools import reduce
import re
import math


YEAR = 2020
DAY = 13

def chinese_remainder(n, a):
    _sum = 0
    prod = reduce(lambda a, b: a*b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        _sum += a_i * mul_inv(p, n_i) * p

    return _sum % prod

def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1

def part_one(_input):
    earliest_time = int(_input[0])
    busses = [int(bus) for bus in _input[1].split(',') if bus != 'x']

    bus_id = min(busses, key=lambda bus: bus - earliest_time % bus)
    return (bus_id - earliest_time % bus_id) * bus_id

def part_two(_input):
    busses = _input[1].split(',')
    n = [int(bus) for bus in busses if bus != 'x']

    a = []
    for i, bus in enumerate(busses):
        if bus == 'x':
            continue
        a.append(i * -1)

    return chinese_remainder(n, a)

if __name__ == '__main__':
    puzzle = Puzzle(year=YEAR, day=DAY)
    _input = puzzle.input_data.split('\n')
    #_input = [line[:-1] for line in open('input', 'r').readlines()]

    1print(part_one(_input))
    print(part_two(_input))

