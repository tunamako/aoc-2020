from aocd import submit
from aocd.models import Puzzle

import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math
from pprint import *

YEAR = 2020
DAY = 7


def contains_shiny(color, bagrules):
    if color == "shiny gold":
        return True

    for bag in bagrules[color]:
        if contains_shiny(bag[0], bagrules):
            return True

    return False


def parse_bagrules(_input):
    # color: [(color, count), ...]
    bagrules = defaultdict(list)

    for rule in _input:
        rule = rule[:-1]
        color, contents = rule.split(' bags contain ')
        
        for c in contents.split(', '):
            if c == "no other bags":
                bagrules[color]
                continue

            content_count = int(c.split(' ')[0])
            content_color = c[c.index(' ')+1:c.index('bag')-1]

            bagrules[color].append( (content_color, content_count) )
 
    return bagrules


def part_one(_input):
    bagrules = parse_bagrules(_input)
    valids = 0

    for color in bagrules:
        if contains_shiny(color, bagrules):
            valids += 1

    return valids - 1


def get_bag_count(color, bagrules):
    if bagrules[color] == []:
        return 1

    count = 0
    for bag in bagrules[color]:
        count += bag[1] * get_bag_count(bag[0], bagrules)

    print(color, count)
    return count + 1


def part_two(_input):
    bagrules = parse_bagrules(_input)
    return get_bag_count("shiny gold", bagrules) - 1


if __name__ == '__main__':
    puzzle = Puzzle(year=YEAR, day=DAY)
    _input = puzzle.input_data.split('\n')
    #_input = [line[:-1] for line in open('input').readlines()]
    #_input = open('bigboy').readlines()

    #print(part_one(_input))
    print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
