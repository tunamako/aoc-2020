from aocd import submit
from aocd.models import Puzzle
    
import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math

YEAR = 2020
DAY = 3

def part_one(_input, xslope=3, yslope=1):
    curX, curY = 0, 0
    trees = 0

    while curY < len(_input):
        if _input[curY][curX % len(_input[0])] == '#':
            trees += 1
        curX += xslope
        curY += yslope

    return trees

def part_two(_input):
    pairs = [(1, 1),(3, 1),(5, 1),(7, 1),(1, 2)]

    return math.prod(part_one(_input, *pair) for pair in pairs)

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
