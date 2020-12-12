from aocd.models import Puzzle

import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math
import numpy as np
import sys

np.set_printoptions(threshold=sys.maxsize)

YEAR = 2020
DAY = 11

DIRECTIONS = list(permutations([-1, 0, 1], 2)) + [(1, 1), (-1, -1)]
SHAPE = None


def get_neighbors_1(x, y, grid):
    count = 0

    for d in DIRECTIONS:
        x_delta = x+d[0]
        y_delta = y+d[1]

        if (0 <=x_delta < SHAPE[0]) and (0 <=y_delta < SHAPE[1]):
            if grid[x_delta][y_delta] == '#':
                count += 1

    return count

def get_neighbors_2(x, y, grid):
    count = 0

    for d in DIRECTIONS:
        x_delta = x+d[0]
        y_delta = y+d[1]

        while (0 <=x_delta < SHAPE[0]) and (0 <=y_delta < SHAPE[1]):
            if grid[x_delta][y_delta] == 'L':
                break
            if grid[x_delta][y_delta] == '#':
                count += 1
                break

            x_delta += d[0]
            y_delta += d[1]


    return count

def next_gen(grid, neighbor_func, threshold):
    tmp = grid.copy()
    for x in range(SHAPE[0]):
        for y in range(SHAPE[1]):
            if grid[x][y] == '.':
                continue

            live_neighbors = neighbor_func(x, y, grid)


            if grid[x][y] == 'L' and live_neighbors == 0:
                tmp[x][y] = '#'
            elif grid[x][y] == '#' and live_neighbors >= threshold:
                tmp[x][y] = 'L'
    
    return tmp


def part_one(_input):
    count = 0
    prev = -1

    while count != prev:
        prev = 0
        _input = next_gen(_input, get_neighbors_1, 4)
        count = np.count_nonzero(_input == '#')

    return count


def part_two(_input):
    while next_gen(_input, get_neighbors_2, 5):
        continue

    return np.count_nonzero(_input == '#')


if __name__ == '__main__':
    puzzle = Puzzle(year=YEAR, day=DAY)
    _input = np.array(list(map(list, puzzle.input_data.split('\n'))))
    #_input = np.array([list(row[:-1]) for row in open('input', 'r').readlines()])
    _input = np.swapaxes(_input, 0, 1)
    SHAPE = np.shape(_input)

    #print(part_one(_input.copy()))
    #print(part_two(_input.copy()))

    _input = _input.copy()
    cProfile.run('print(part_one(_input))')
    #_input = _input.copy()
    #cProfile.run('print(part_two(_input))')
