import numpy as np
from aocd import submit
from aocd.models import Puzzle

def a(data):
    sum = 0
    for line in data.split("\n"):
        numbers = np.array([int(x) for x in line.split()])
        diff = np.diff(numbers)
        last_numbers = [numbers[-1], diff[-1]]
        pyramid = [diff]
        while diff.any():
            diff = np.diff(diff)
            pyramid.append(diff)
            last_numbers.append(diff[-1])
        sum += np.sum(last_numbers)
    return sum

def add_back(last_numbers):
    val = 0
    for number in reversed(last_numbers):
        val = number - val
    return val


def b(data):
    sum = 0
    for line in data.split("\n"):
        numbers = np.array([int(x) for x in line.split()])
        diff = np.diff(numbers)
        last_numbers = [numbers[0], diff[0]]
        pyramid = [diff]
        while diff.any():
            diff = np.diff(diff)
            pyramid.append(diff)
            last_numbers.append(diff[0])
        sum += add_back(last_numbers)
    return sum


year = 2023
day = 9

p = Puzzle(year=year, day=day)
data = p.input_data

example_data_a = p.examples[0].input_data
example_answer_a = int(p.examples[0].answer_a)

assert(a(example_data_a)==example_answer_a)
assert(a(data)==1647269739)
# submit(a(data), part="a", year=year, day=day)


example_data_b = example_data_a
example_answer_b = 2

assert(b(example_data_b)==example_answer_b)
assert(b(data)==864)
# submit(b(data), part="b", year=year, day=day)
