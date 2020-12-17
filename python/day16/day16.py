from aocd.models import Puzzle

import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math


YEAR = 2020
DAY = 16


def get_rules(rules):
    tmp = dict()
    for rule in rules.split('\n'):
        name, rule = rule.split(': ')
        first, second = rule.split(' or ')

        first = tuple(map(int, first.split('-')))
        second = tuple(map(int, second.split('-')))

        tmp[name] = (first[0], first[1], second[0], second[1])

    return tmp


def parse_input(_input):
    rules, ticket, nearby = _input
    rules = get_rules(rules)
    ticket = list(map(int, ticket.split('\n')[1].split(',')))
    nearby = [list(map(int, t.split(','))) for t in nearby.split('\n')[1:]]

    return rules, ticket, nearby


def satisfies_rule(value, rule):
    return ((rule[0] <= value <= rule[1]) or (rule[2] <= value <= rule[3]))


def invalid(ticket, rules):
    for value in ticket:
        if not any([satisfies_rule(value, rule) for rule in rules.values()]):
            return True, value

    return False, 0


def match_rulesold(index, used_rules, possible_rules, ticket_len, rules):
    if index >= ticket_len:
        return []

    for rule_name in possible_rules[index]:
        if rule_name in used_rules:
            continue

        ret = match_rules(index + 1, used_rules | {rule_name}, possible_rules, ticket_len, rules)
        if ret is not None:
            return [rule_name] + ret

    return None


def match_rules(possible_rules, ticket_len, rules):
    matched_columns = dict()

    while len(matched_columns) < ticket_len:
        for i in range(ticket_len):
            if i in matched_columns:
                continue

            if len(possible_rules[i]) == 1:
                matched_columns[i] = possible_rules[i].pop()

                for j in range(ticket_len):
                    if matched_columns[i] in possible_rules[j]:
                        possible_rules[j].remove(matched_columns[i])


    return matched_columns

def part_one(_input):
    rules, ticket, nearby = parse_input(_input)
 
    return sum([invalid(t, rules)[1] for t in nearby])


def part_two(_input):
    rules, ticket, nearby = parse_input(_input)

    nearby = [t for t in nearby if not invalid(t, rules)[0]]
    possible_rules = defaultdict(set)

    for name, rule in rules.items():
        for i in range(len(ticket)):
            if all([satisfies_rule(t[i], rule) for t in nearby]):
                possible_rules[i].add(name)

    rule_indices = match_rules(possible_rules, len(ticket), rules)

    return math.prod([ticket[i] for i, rule in rule_indices.items() if 'departure' in rule])


if __name__ == '__main__':
    puzzle = Puzzle(year=YEAR, day=DAY)
    _input = puzzle.input_data.split('\n\n')
    #_input = open('input').read().split('\n\n')

    #print(part_one(_input))
    #print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    cProfile.run('print(part_two(_input))')
