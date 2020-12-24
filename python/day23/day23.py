from aocd.models import Puzzle

import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math
import llist
import time

YEAR = 2020
DAY = 23


class Cup(object):

    def __init__(self, value, _next=None, prev=None):
        self.value = value
        self.next = _next
        self.prev = prev

    def __repr__(self):
        return str(self.value)

    def traverse(self, tail):
        if self is not tail:
            return [self.value] + self.next.traverse(tail)
        else:
            return [self.value]

class Circle(object):

    def __init__(self, circle):
        self.head = Cup(circle[0])
        self.value_reference = {
            self.head.value: self.head
        }

        prev = self.head
        for c in circle[1:]:
            c = Cup(c, prev=prev)
            self.value_reference[c.value] = c
            prev.next = c
            prev = c
        self.tail = prev

        self.head.prev = self.tail
        self.tail.next = self.head

        self.cur = self.head
        self.size = len(circle)

    def __repr__(self):
        return str(self.head.traverse(self.tail))       

    def as_list(self):
        return self.head.traverse(self.tail)

    def rotate(self):
        self.tail = self.head
        self.head = self.head.next

    def remove(self, cup):
        cup.prev.next = cup.next
        cup.next.prev = cup.prev

        if cup is self.tail:
            self.tail = self.tail.prev
        elif cup is self.head:
            self.head = self.head.next
  
        return cup

    def insert(self, cup, new_cup):
        new_cup.next = cup.next
        new_cup.prev = cup
        cup.next = new_cup
        new_cup.next.prev = new_cup

        if cup is self.tail:
            self.tail = new_cup

    def get_dest(self, removed_vals):
        if self.cur.value > 1 and self.cur.value - 1 not in removed_vals:
            return self.cur.value - 1

        for i in range(self.cur.value - 1, 0, -1):
            if i not in removed_vals:
                return i

        for i in range(self.size, self.cur.value, -1):
            if i not in removed_vals:
                return i

    def move(self):
        removed = [self.remove(self.cur.next) for i in range(3)]

        dest = self.get_dest(set([c.value for c in removed]))

        for i in range(3):
            self.insert(self.value_reference[dest], removed[-i])

        self.cur = self.cur.next


def part_one(_input):
    circle = Circle(_input)

    for i in range(100):
        circle.move()

    while circle.head.value != 1:
        circle.rotate()

    return ''.join([str(c) for c in circle.as_list()[1:]])

def part_two(_input):
    circle = Circle(_input + [i for i in range(10, 1000001)])

    for i in range(10000000):
        circle.move()

    cup_one = circle.value_reference[1].next.value
    cup_two = circle.value_reference[1].next.next.value

    print(cup_one, cup_two)
    return cup_one * cup_two

if __name__ == '__main__':
    _input = "562893147"
    #_input = "389125467"
    #_input = "312546"

    _input = list(map(int, _input))
    #print(part_one(_input))
    #print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    cProfile.run('print(part_two(_input))')
