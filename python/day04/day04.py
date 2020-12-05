from aocd import submit
from aocd.models import Puzzle

import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re

import math
from pprint import *

YEAR = 2020
DAY = 4


def isvalid(passport):
    fields = {"byr","iyr","eyr","hgt","hcl","ecl","pid",}
    eyes = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}

    if not (len(fields.intersection(passport.keys())) == 7):
        return False
    if not (1920 <= int(passport['byr']) <= 2002):
        return False
    if not (2010 <= int(passport['iyr']) <= 2020):
        return False
    if not (2020 <= int(passport['eyr']) <= 2030):
        return False
    if not ((passport['hgt'][-2:] == 'cm' and 150 <= int(passport['hgt'][:-2]) <= 193) or (passport['hgt'][-2:] == 'in' and 59 <= int(passport['hgt'][:-2]) <= 76)):
        return False
    if not ((passport['hcl'][0] == '#') and (len(passport['hcl'])==7) and (passport['hcl'][1:].isalnum())):
        return False
    if not (passport['ecl'] in eyes):
        return False
    if not ((len(passport['pid']) == 9) and (passport['pid'].isnumeric())):
        return False

    return True


def part_one(_input):
    passes = []
    curpass = dict()

    for line in _input:
        if line == '':
            passes.append(curpass)
            curpass = dict()
            continue
        else:
            items = line.split(' ')
            for i in items:
                key, val = i.split(':')
                curpass[key] = val

    valids = 0
    for p in passes:
        if isvalid(p):
            valids += 1
    return valids

def part_two(_input):
    pass


if __name__ == '__main__':
    puzzle = Puzzle(year=YEAR, day=DAY)
    #_input = puzzle.input_data.split('\n')
    _input = [line[:-1] for line in open('input', 'r').readlines()]
    #_input = open('bigboy').readlines()

    print(part_one(_input))
    #print(part_two(_input))

    #submit(part_one(_input), part="a", day=DAY, year=YEAR)
    #submit(part_two(_input), part="b", day=DAY, year=YEAR)

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
