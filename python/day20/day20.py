from aocd.models import Puzzle

import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math
import numpy as np
from pprint import *

YEAR = 2020
DAY = 20


def part_one(_input):
    tiles = dict()

    for tile in _input:
        tile = tile.split('\n')
        _id = tile[0].split(' ')[1][:-1]

        edges = {tile[1], tile[-1]}
        left = []
        right = []

        for row in tile[1:]:
            left.append(row[0])
            right.append(row[-1])

        edges.add(''.join(left))
        edges.add(''.join(right))

        tiles[_id] = edges

    res = 1
    for _id, edges in tiles.items():
        matchcount = 0
        for edge in edges:
            for i, e in tiles.items():
                if i == _id:
                    continue
                elif edge in e or edge[::-1] in e:
                    matchcount += 1
                    break

        if matchcount == 2:
            res *= int(_id)

    return res


class Tile(object):

    def __init__(self, raw_tile):
        tile = raw_tile.split('\n')
        self._id = tile[0].split(' ')[1][:-1]
        self.tile = np.array([list(row) for row in tile[1:]])
        self.neighbors = {"u": None,"d": None,"l": None,"r": None}

        r = np.rot90
        self.transforms = [
            self.tile,
            r(self.tile),
            r(r(self.tile)),
            r(r(r(self.tile))),
            np.flipud(self.tile),
            np.fliplr(self.tile),
            r(np.flipud(self.tile)),
            r(np.fliplr(self.tile)),
        ]

    def __repr__(self):
        return self._id

    def find_neighbors(self, tiles):
        found = []
        for d in self.neighbors:
            if self.neighbors[d]:
                continue

            for t in tiles:
                if t is self:
                    continue
                elif t in self.neighbors.values():
                    continue
                elif self.matches(t, d):
                    found.append(t)
                    break

        return found

    def matches(self, tile, direction):
        d_slices = {
            'u': ('d', 0, -1),
            'd': ('u', -1, 0),
            'l': ('r', 0, -1),
            'r': ('l', -1, 0)
        }
        sl = d_slices[direction]

        for i, t in enumerate(tile.transforms):
            if direction in 'ud':
                ours, theirs = self.tile[sl[1]], t[sl[2]]
            else:
                ours, theirs = self.tile[:,sl[1]], t[:,sl[2]]

            if np.array_equal(ours, theirs):
                self.set_match(tile, direction, i)
                tile.set_match(self, sl[0], i)
                return True

        return False

    def set_match(self, tile, direction, t_index):
        self.neighbors[direction] = tile

        if len(self.transforms) != 1:
            self.tile = self.transforms[t_index]

        self.transforms = [self.tile]

    def get_transforms(self):
        if self.matched:
            return [self.tile]
        else:
            return self.transforms

    def remove_borders(self):
        self.tile = self.tile[1:-1,1:-1]

    def stitch_right(self):
        right = self.neighbors['r']
        if right:
            return np.concatenate((self.tile, right.stitch_right()), axis=1)
        else:
            return self.tile

def has_monster(x, y, grid):
    relative_coords = [
        (0, -1),
        (1, -2),
        (4, -2),
        (5, -1),
        (6, -1),
        (7, -2),
        (10, -2),
        (11, -1),
        (12, -1),
        (13, -2),
        (16, -2),
        (17, -1),
        (18, 0),
        (18, -1),
        (19, -1),
    ]

    ret = set()
    for i, j in relative_coords:
        if grid[y+j][x+i] != '#':
            return set()
        else:
            ret.add((x+i, y+j))

    return ret

def part_two(_input):
    tiles = [Tile(tile) for tile in _input]

    n = [tiles[0]]
    while n:
        n += n.pop().find_neighbors(tiles)

    # find top left corner
    upper_left = tiles[0]
    while True:
        if upper_left.neighbors['u']:
            upper_left = upper_left.neighbors['u']
        elif upper_left.neighbors['l']:
            upper_left = upper_left.neighbors['l']
        else:
            break

    for tile in tiles:
        tile.remove_borders()

    #stich row by row
    t = upper_left
    grid = t.stitch_right()
    t = t.neighbors['d']

    while t:
        grid = np.concatenate((grid, t.stitch_right()), axis=0)
        t = t.neighbors['d']

    r = np.rot90
    grid_transforms = [
        grid,
        r(grid),
        r(r(grid)),
        r(r(r(grid))),
        np.flipud(grid),
        np.fliplr(grid),
        r(np.flipud(grid)),
        r(np.fliplr(grid)),
    ]

    #find monster
    sea_monster_coords = set()
    for t in grid_transforms:
        for i in range(len(grid) - 18):
            for j in range(len(grid) - 1):
                sea_monster_coords |= has_monster(i, j, t)

    return np.sum(grid == '#') - len(sea_monster_coords)


if __name__ == '__main__':
    puzzle = Puzzle(year=YEAR, day=DAY)
    _input = puzzle.input_data.split('\n\n')
    #_input = open('input').read().split("\n\n")

    #print(part_one(_input))
    #print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    cProfile.run('print(part_two(_input))')
