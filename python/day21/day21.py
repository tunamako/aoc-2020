from aocd.models import Puzzle

import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math


YEAR = 2020
DAY = 21


def part_one(_input):
    foods = []
    all_ing = set()
    all_allerg = set()
    for line in _input:
        if '(' in line:
            ing, allergs = line.split(' (contains')
            allergs = set(allergs[1:-1].split(', '))
        else:
            ing = line
            allergs = set()

        ing = set(ing.split(' '))
        foods.append([ing, allergs])
        all_ing |= ing
        all_allerg |= allergs

    common = dict()

    for a in all_allerg:
        otherfoods = []

        for food in foods:
            if a in food[1]:
                otherfoods.append(food)

        common_ing = set.intersection(*[food[0] for food in otherfoods])
        common[a] = common_ing

    found_allergens = {
        "eggs": "qxfzc",
        "dairy": "vmhqr",
        "peanuts": "xrmxxvn",
        "wheat": "jxh",
        "fish": "khpdjv",
        "soy": "rdfr",
        "sesame": "rfmvh",
        "nuts": "gnrpml",
    }

    all_ing -= set(found_allergens.values())
    ret = 0
    for ing in all_ing:
        for food in foods:
            if ing in food[0]:
                ret += 1
    return ret

def part_two(_input):
    found_allergens = {
        "eggs": "qxfzc",
        "dairy": "vmhqr",
        "peanuts": "xrmxxvn",
        "wheat": "jxh",
        "fish": "khpdjv",
        "soy": "rdfr",
        "sesame": "rfmvh",
        "nuts": "gnrpml",
    }

    allergs = sorted(found_allergens.keys())
    return ','.join([found_allergens[a] for a in allergs])

if __name__ == '__main__':
    puzzle = Puzzle(year=YEAR, day=DAY)
    _input = puzzle.input_data.split('\n')
    #_input = [line[:-1] for line in open('input').readlines()]

    print(part_one(_input))
    print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
