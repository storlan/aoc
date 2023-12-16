from aocd import submit
from aocd.models import Puzzle
import re
from collections import defaultdict

def hash(string):
    value = 0
    for c in string:
        value += ord(c)
        value *= 17
        value = value % 256
    return value

def a(data):
    sum = 0
    for string in data.split(","):
        sum += hash(string)
    return sum

def b(data):
    sum = 0
    hash_map = defaultdict(dict)
    for string in data.split(","):
        parts = re.split("=|-", string)
        label = parts[0]
        box = hash(label)
        if len(parts[-1]) == 0:
            try:
                hash_map[box].pop(label)
            except KeyError:
                pass
        else:
            hash_map[box][label] = int(parts[1])
    for i, d in hash_map.items():
        if len(d) == 0:
            continue
        for j, val in enumerate(d.values()):
            sum += (i+1) * (j+1) * val


    return sum

year = 2023
day = 15

p = Puzzle(year=year, day=day)
data = p.input_data

example_data_a = p.examples[0].input_data
example_answer_a = p.examples[0].answer_a

assert(a(example_data_a)==int(example_answer_a))
assert(a(data)==505459)
#submit(a(data), part="a", year=year, day=day)

example_data_b = example_data_a
example_answer_b = 145

assert(b(example_data_b)==example_answer_b)
assert(b(data)==228508)
#submit(b(data), part="b", year=year, day=day)
