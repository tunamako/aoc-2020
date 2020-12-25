from aocd.models import Puzzle

import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math


YEAR = 2020
DAY = 25


def transform(subj, loop_size):
	ret = 1
	for i in range(loop_size):
		ret *= subj
		ret = ret % 20201227

	return ret

def part_one(_input):
	card_key = int(_input[0])
	door_key = int(_input[1])

	i = 0
	key = 1
	while key != card_key:
		i += 1
		key *= 7
		key = key % 20201227


	return transform(door_key, i)


if __name__ == '__main__':
    puzzle = Puzzle(year=YEAR, day=DAY)
    _input = puzzle.input_data.split('\n')
    #_input = open('bigboy').readlines()

    print(part_one(_input))
    print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
