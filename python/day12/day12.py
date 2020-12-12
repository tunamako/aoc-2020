from aocd.models import Puzzle

import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math

from abc import ABC


YEAR = 2020
DAY = 12

Point = namedtuple("Point", ['x', 'y']) 


class AbstractShip(ABC):
    TRANSLATIONS = [
        (0, 1),  # N
        (1, 0),  # E
        (0, -1), # S
        (-1, 0), # W
    ]
    ROTATIONS = {
        "L": lambda p: Point(-1 * p.y, p.x),
        "R": lambda p: Point(p.y, -1 * p.x)
    }

    def __init__(self, instructions):
        self.pos = Point(0,0)
        self.waypoint = Point(10, 1)
        self.facing = 1
        self.instructions = instructions

    def parse_instructions(self):
        for line in self.instructions:
            action, value = line[0], int(line[1:])

            if action in "NESW":
                self.step("NESW".index(action), value)
            elif action in "LR":
                self.turn(action, int(value/90))
            elif action == "F":
                self.step_forward(value)


class Ship1(AbstractShip):
    def step(self, direction, count):
        move = self.TRANSLATIONS[direction]

        self.pos = Point(self.pos.x + (count * move[0]),
                         self.pos.y + (count * move[1]))

    def step_forward(self, count):
        self.step(self.facing, count)

    def turn(self, direction, degrees):
        if direction == 'L':
            degrees *= -1

        self.facing = (self.facing + degrees) % 4


class Ship2(AbstractShip):
    def step(self, direction, count):
        move = self.TRANSLATIONS[direction]

        self.waypoint = Point(self.waypoint.x + (count * move[0]),
                              self.waypoint.y + (count * move[1]))

    def step_forward(self, count):
        self.pos = Point(self.pos.x + (self.waypoint.x * count),
                         self.pos.y + (self.waypoint.y * count))

    def turn(self, direction, degrees):
        for i in range(degrees):
            self.waypoint = self.ROTATIONS[direction](self.waypoint)


def part_one(_input):
    ship = Ship1(_input)
    ship.parse_instructions()

    return sum(map(abs, ship.pos))

def part_two(_input):
    ship = Ship2(_input)
    ship.parse_instructions()

    return sum(map(abs, ship.pos))



if __name__ == '__main__':
    puzzle = Puzzle(year=YEAR, day=DAY)
    _input = puzzle.input_data.split('\n')
    #_input = [line[:-1] for line in open('input', 'r').readlines()]
    #_input = open('bigboy').readlines()

    print(part_one(_input))
    print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
