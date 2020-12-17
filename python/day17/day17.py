from aocd.models import Puzzle

import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain, product
import itertools
import re
import math
import numpy as np
from pprint import *
import time

YEAR = 2020
DAY = 17


class CubeAutomaton(object):

    def __init__(self, plane):
        self.plane = plane

    def execute(self, dims):
        self.dims = dims
        self.directions = list(itertools.product([-1, 0, 1], repeat=dims))
        self.directions.remove(tuple([0]*dims))
        self.active = set()

        for i in range(np.shape(self.plane)[0]):
            for j in range(np.shape(self.plane)[1]):
                if self.plane[i][j] == '#':
                    self.active.add((i, j) + tuple([0]*(dims-2)))

        for i in range(6):
            self.next_gen()

        return len(self.active)

    def next_gen(self):
        relevant_neighbors = set.union(*[self.get_all_neighbors(cube) for cube in self.active])

        to_add = set()
        to_remove = set()

        for cube in relevant_neighbors:
            live_neighbors = self.get_active_neighbor_count(cube)

            if (cube in self.active) and (live_neighbors not in [2,3]):
                to_remove.add(cube)
            elif (cube not in self.active) and (live_neighbors == 3):
                to_add.add(cube)

        self.active |= to_add
        self.active -= to_remove

    def get_all_neighbors(self, cube):
        neighbors = set()
        for d in self.directions:
            neighbors.add(tuple([cube[n]+d[n] for n in range(self.dims)]))
        neighbors.add(cube)

        return neighbors

    def get_active_neighbor_count(self, cube):
        count = 0
        for d in self.directions:
            if tuple([cube[n]+d[n] for n in range(self.dims)]) in self.active:
                count += 1

        return count


def part_one(_input):
    return CubeAutomaton(_input).execute(3)


def part_two(_input):
    return CubeAutomaton(_input).execute(4)


if __name__ == '__main__':
    puzzle = Puzzle(year=YEAR, day=DAY)
    _input = np.array(list(map(list, puzzle.input_data.split('\n'))))
    #_input = np.array([list(row[:-1]) for row in open('input', 'r').readlines()])
    _input = np.swapaxes(_input, 0, 1)

    print(part_one(_input))
    print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
