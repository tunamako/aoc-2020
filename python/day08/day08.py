from aocd import submit
from aocd.models import Puzzle

import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math

YEAR = 2020
DAY = 8


class AdventMachine(object):

	def acc(self, delta):
		self.accumulator += delta
		self.ip += 1

	def jmp(self, delta):
		self.ip += delta

	def nop(self, delta):
		self.ip += 1

	def __init__(self, tape):
		self.opcodes = {
			"acc": self.acc,
			"jmp": self.jmp,
			"nop": self.nop,
		}
		self.tape = tape.copy()
		self.accumulator = 0
		self.ip = 0

	def reinit(self, tape):
		self.tape = tape.copy()
		self.accumulator = 0
		self.ip = 0

	def parse_cmd(self, cmd):
		op = cmd.split(' ')[0]
		delta = int(cmd.split(' ')[1][1:])

		if '-' in cmd:
			delta *= -1

		return op, delta

	def execute(self, halt_on_loop=True):
	    seen = set()

	    while True:
	    	if self.ip in seen:
	    		return halt_on_loop
	    	elif self.ip == len(self.tape):
	    		return self.accumulator

	    	seen.add(self.ip)
	    	cmd = self.tape[self.ip]
	    	op, delta = self.parse_cmd(cmd)

	    	self.opcodes[op](delta)


def part_one(_input):
	machine = AdventMachine(_input)
	machine.execute()
	return machine.accumulator

def part_two(_input):
	machine = AdventMachine(_input)

	for i, line in enumerate(_input):
		if line[:3] == "acc":
			continue
		elif line[:3] == "jmp":
			_input[i] = line.replace("jmp", "nop")
		elif line[:3] == "nop":
			_input[i] = line.replace("nop", "jmp")			

		machine.reinit(_input)

		if acc := machine.execute(halt_on_loop=False):
			return acc
		else:
			_input[i] = line


if __name__ == '__main__':
    puzzle = Puzzle(year=YEAR, day=DAY)
    _input = puzzle.input_data.split('\n')
    #_input = open('bigboy').readlines()

    print(part_one(_input))
    print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
