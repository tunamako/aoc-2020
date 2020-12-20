from aocd.models import Puzzle

import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math


YEAR = 2020
DAY = 18


def evaluate(expr):
	ops = list(filter(lambda s: s in '*+', expr))

	for i, op in enumerate(ops):
		op_index = expr.index(op)

		try:
			nextop_index = expr[op_index+1:].index(ops[i+1]) + op_index + 1
		except:
			nextop_index = len(expr)

		lhs = int(expr[:op_index])
		rhs = int(expr[op_index+1:nextop_index])

		if op == '*':
			lhs = lhs * rhs
		elif op == '+':
			lhs = lhs + rhs

		if nextop_index != len(expr):
			expr = str(lhs) + expr[nextop_index:]
		else:
			expr = str(lhs)

	return expr

def parenthesize_addops(expr):
	for mulop in re.findall(r'\d+\+\d+', expr):
		expr = expr.replace(mulop, '({})'.format(mulop))
	for mulop in re.findall(r'\d+\+\([^\)]+\)', expr):
		expr = expr.replace(mulop, '({})'.format(mulop))
	for mulop in re.findall(r'\([^\)]+\)\+\d+', expr):
		expr = expr.replace(mulop, '({})'.format(mulop))

	return expr

def parse(expr, part2=False):
	if part2:
		expr = parenthesize_addops(expr)

	res = re.findall(r'\([^()]*\)', expr)

	for paren in res:
		expr = expr.replace(paren, evaluate(paren[1:-1]))

	return expr if '(' not in expr else parse(expr, part2)

def part_one(_input):
	_input = [''.join(filter(lambda s: s != ' ', line)) for line in _input]
	count = 0
	for line in _input:
		count += int(parse('({})'.format(line)))

	return count

def part_two(_input):
	_input = [''.join(filter(lambda s: s != ' ', line)) for line in _input]
	count = 0
	for line in _input:
		tmp = int(parse('({})'.format(line), part2=True))
		print(tmp)
		count += tmp
	return count


if __name__ == '__main__':
    puzzle = Puzzle(year=YEAR, day=DAY)
    _input = puzzle.input_data.split('\n')
    #_input = [line[:-1] for line in open('input').readlines()]

    #print(part_one(_input))
    print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
