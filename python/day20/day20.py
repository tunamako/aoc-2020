from aocd.models import Puzzle

import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math
import numpy as np
from pprint import *
import time

YEAR = 2020
DAY = 20


def get_transforms(array):
    r = np.rot90
    return [
        array,
        r(array),
        r(r(array)),
        r(r(r(array))),
        np.flipud(array),
        np.fliplr(array),
        r(np.flipud(array)),
        r(np.fliplr(array)),
    ]


class Tile(object):

    def __init__(self, raw_tile):
        tile = raw_tile.split('\n')
        self._id = tile[0].split(' ')[1][:-1]
        self.tile = np.array([list(row) for row in tile[1:]])
        self.neighbors = {"u": None,"d": None,"l": None,"r": None}

        self.edges = {tile[1], tile[-1]}
        self.edges |= {tile[1][::-1], tile[-1][::-1]}
        self.edges.add(''.join(self.tile[:,0]))
        self.edges.add(''.join(self.tile[:,-1]))
        self.edges.add(''.join(self.tile[:,0])[::-1])
        self.edges.add(''.join(self.tile[:,-1])[::-1])

        self.transforms = get_transforms(self.tile)

    def __repr__(self):
        return self._id

    def find_neighbors(self, tiles):
        # Prefill by finding all four neighbors quickly
        neighbors = set()
        for t in tiles:
            for e in self.edges:
                if e in t.edges:
                    neighbors.add(t)
                    break

        # Figure out their orientation
        found = []
        for d in self.neighbors:
            if self.neighbors[d]:
                continue

            for t in neighbors:
                if t is self:
                    continue
                elif t in self.neighbors.values():
                    continue
                elif self.matches(t, d):
                    found.append(t)
                    break

        return found

    def matches(self, tile, direction):
        d_slices = {'u': ('d', 0, -1),'d': ('u', -1, 0),
                    'l': ('r', 0, -1),'r': ('l', -1, 0)}
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

    def remove_borders(self):
        self.tile = self.tile[1:-1,1:-1]

    def stitch_right(self):
        right = self.neighbors['r']
        if right:
            return np.concatenate((self.tile, right.stitch_right()), axis=1)
        else:
            return self.tile

    def stitch(self):
        row = self.stitch_right()
        down = self.neighbors['d']
        if down:
            return np.concatenate((row, down.stitch()), axis=0)
        else:
            return row


def part_one(_input):
    tiles = [Tile(tile) for tile in _input]

    n = [tiles[0]]
    while n:
        n += n.pop().find_neighbors(tiles)

    res = 1
    for tile in tiles:
        matchcount = sum([n is None for n in tile.neighbors.values()])
        if matchcount == 2:
            res *= int(tile._id)

    return res

relative_coords = [(0, -1),(1, -2),(4, -2),(5, -1),(6, -1),
                   (7, -2),(10, -2),(11, -1),(12, -1),(13, -2),
                   (16, -2),(17, -1),(18, 0),(18, -1),(19, -1),]

def has_monster(x, y, grid):
    for i, j in relative_coords:
        if grid[y+j][x+i] != '#':
            return False

    return True

def part_two(_input):
    tiles = [Tile(tile) for tile in _input]

    n = [tiles[0]]
    while n:
        n += n.pop().find_neighbors(tiles)

    # find top left corner
    u_l = tiles[0]
    while u_l.neighbors['u'] or u_l.neighbors['l']:
        if u_l.neighbors['u']:
            u_l = u_l.neighbors['u']
        elif u_l.neighbors['l']:
            u_l = u_l.neighbors['l']

    for tile in tiles:
        tile.remove_borders()

    #stich row by row
    grid = u_l.stitch()
    grid_transforms = get_transforms(grid)

    #find monster
    sea_monster_count = 0
    for t in grid_transforms:
        for i in range(len(grid) - 18):
            for j in range(len(grid) - 1):
                if has_monster(i, j, t):
                    sea_monster_count += 1

        if sea_monster_count:
            return np.sum(grid == '#') - (sea_monster_count * 15)


if __name__ == '__main__':
    puzzle = Puzzle(year=YEAR, day=DAY)
    _input = puzzle.input_data.split('\n\n')
    #_input = open('input').read().split("\n\n")

    #print(part_one(_input))
    #print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    cProfile.run('print(part_two(_input))')
