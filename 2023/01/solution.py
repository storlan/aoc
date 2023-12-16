from aocd import submit
from aocd.models import Puzzle

import re

def a(data):
    sum = 0
    for s in data.split("\n"):
        numbers = re.findall(r"\d", s)
        sum += (int(numbers[0] + numbers[-1]))
    return sum

def b(data):
    values = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    number_map = {number:i + 1 for i, number in enumerate(values)}
    regex = rf"(?=(\d|{'|'.join(values)}))"
    sum = 0
    for s in data.split("\n"):
        numbers = re.findall(regex, s)
        first = str(number_map[numbers[0]]) if numbers[0] in number_map else numbers[0]
        last = str(number_map[numbers[-1]]) if numbers[-1] in number_map else numbers[-1]
        new_val = int(first + last)
        sum += new_val
    return sum

year = 2023
day = 1

p = Puzzle(year=year, day=day)
data = p.input_data

example_data_a = p.examples[0].input_data
example_answer_a = p.examples[0].answer_a


assert(a(example_data_a)==int(example_answer_a))
assert(a(data)==55108)
# submit(a(data), part="a", year=year, day=day)


example_data_b = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""
example_answer_b = 281

assert(b(example_data_b)==int(example_answer_b))
assert(b(data)==56324)
# submit(b(data), part="b", year=year, day=day)
