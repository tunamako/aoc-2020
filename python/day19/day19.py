from aocd.models import Puzzle

import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math


YEAR = 2020
DAY = 19

global STRING_CACHE
STRING_CACHE = defaultdict(set)


class LeafRule(object):

    def __init__(self, _id, _str):
        self.id = _id
        self.str = _str

    def __repr__(self):
        return "LeafRule " + self.id

    def rule_matches(self, string):
        return string == self.str


class Rule(object):

    def __init__(self, _id, all_rulestrings, all_rules, part2=False):
        self.id = _id
        self.rule_options = []
        
        options = all_rulestrings[_id].split(' | ')
        for s in options:
            subrule = []
            for i in s.split(' '):
                if i in all_rules:
                    pass
                elif all_rulestrings[i].isalpha():
                    all_rules[i] = LeafRule(i, all_rulestrings[i])
                elif i not in all_rules:
                    if part2 and i == "11":
                        all_rules[i] = Rule11(i, all_rulestrings, all_rules, part2)
                    elif part2 and i == "8":
                        all_rules[i] = Rule8(i, all_rulestrings, all_rules, part2)
                    else:
                        all_rules[i] = Rule(i, all_rulestrings, all_rules, part2)

                subrule.append(all_rules[i])

            self.rule_options.append(subrule)

    def __repr__(self):
        return "Rule " + self.id

    def rule_matches(self, string):
        if string not in STRING_CACHE:
            STRING_CACHE[string] = [set(), set()]
        elif self.id in STRING_CACHE[string][0]:
            return False
        elif self.id in STRING_CACHE[string][1]:
            return True

        result = any(self.option_matches(option, string) for option in self.rule_options)

        STRING_CACHE[string][result].add(self.id)

        return result

    def option_matches(self, option, string):
        if len(option) == 1:
            return option[0].rule_matches(string)

        for i in range(1, len(string)):
            if (option[0].rule_matches(string[:i]) and \
                option[1].rule_matches(string[i:])):

                return True

        return False


class Rule8(Rule):
    
    def __init__(self, _id, all_rulestrings, all_rules, part2=False):
        super().__init__(_id, all_rulestrings, all_rules, part2)

        self.rule_options[1].append(self)


class Rule11(Rule):

    def __init__(self, _id, all_rulestrings, all_rules, part2=False):
        super().__init__(_id, all_rulestrings, all_rules, part2)

        self.rule_options[1].insert(1, self)

    def option_matches(self, option, string):
        if len(option) != 3:
            return super().option_matches(option, string)

        for i in range(1, len(string) - 1):
            for j in range(i + 1, len(string)):
                if (option[0].rule_matches(string[:i]) and \
                    option[1].rule_matches(string[i:j]) and \
                    option[2].rule_matches(string[j:])):

                    return True

        return False


def format_input(rules, messages):
    tmp = rules.split('\n')
    rules = dict()
    for r in tmp:
        key, val = r.split(': ')
        rules[key] = ''.join(list(filter(lambda s: s!='\"', val)))
    messages = messages.split('\n')

    return rules, messages

def part_one(_input):
    STRING_CACHE.clear()

    rules, messages = format_input(*_input)
    root = Rule('0', rules, dict())

    return sum([root.rule_matches(msg) for msg in messages])

def part_two(_input):
    STRING_CACHE.clear()

    rules, messages = format_input(*_input)
    rules['8'] = "42 | 42"
    rules['11'] = "42 31 | 42 31"
    root = Rule('0', rules, dict(), part2=True)

    return sum([root.rule_matches(msg) for msg in messages])


if __name__ == '__main__':
    puzzle = Puzzle(year=YEAR, day=DAY)
    _input = puzzle.input_data.split('\n\n')
    #_input = open('input').read().split('\n\n')

    print(part_one(_input))
    print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
