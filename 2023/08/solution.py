from aocd import submit
from aocd.models import Puzzle

import re

def a(data):
    regex = r"([A-Z]+) = \(([A-Z]+), ([A-Z]+)\)"
    lines = data.split("\n")
    instructions = lines[0]
    entries = {}
    for line in lines[2:]:
        match = re.search(regex, line)
        key, vall, valr = match.groups()
        entries[key] = (vall, valr)
    current = "AAA"
    steps = 0
    while current != "ZZZ":
        for instruction in instructions:
            if instruction == "R":
                current = entries[current][1]
            else:
                current = entries[current][0]
            steps += 1
            if current == "ZZZ":
                break
    return steps

def done(current_values):
    for val in current_values:
        if val[2] != "Z":
            return False
    return True

def get_factors(number):
    i = 2
    factors = []
    while i <= number:
        if (number % i) == 0:
            factors.append(i)
            number = number / i
        else:
            i = i + 1
    return factors

def find_common_primes(numbers):
    factors = set()
    for number in list(numbers):
        new_factors = set(get_factors(number))
        factors |= new_factors
    return factors

def b(data):
    steps = 0
    regex = r"([A-Z0-9]+) = \(([A-Z0-9]+), ([A-Z0-9]+)\)"
    lines = data.split("\n")
    instructions = lines[0]
    entries = {}
    current_values = []
    for line in lines[2:]:
        match = re.search(regex, line)
        key, vall, valr = match.groups()
        entries[key] = (vall, valr)
        if key[2] == "A":
            current_values.append(key)
    step_to_z_map = {}
    for val in current_values:
        current = val
        tries = 0
        while val not in step_to_z_map :
            for instruction in instructions:
                if instruction == "R":
                    current = entries[current][1]
                else:
                    current = entries[current][0]
                tries += 1
                if current[2] == "Z":
                    step_to_z_map[val] = tries
                    break
    factors = find_common_primes(step_to_z_map.values())
    steps = 1
    for factor in factors:
        steps *= factor
    return steps


year = 2023
day = 8

p = Puzzle(year=year, day=day)
data = p.input_data

example_data_a = p.examples[0].input_data
example_answer_a = 2

assert(a(example_data_a)==example_answer_a)
assert(a(data)==17263)
#submit(a(data), part="a", year=year, day=day)


example_data_b = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""
example_answer_b = 6

assert(b(example_data_b)==example_answer_b)
assert(b(data)==14631604759649)
#submit(b(data), part="b", year=year, day=day)
