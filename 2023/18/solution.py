from aocd import submit
from aocd.models import Puzzle

from scipy.ndimage import binary_fill_holes
import numpy as np
import re

instruction_re = r"([UDRL]) ([0-9]+) \(#([0-9a-f]+)\)"

direction_map = {
    "U":(-1,0),
    "D":(1,0),
    "L":(0,-1),
    "R":(0,1)
}

def a(data):
    start = (0,0)
    min_r = 0
    min_c = 0
    max_r = 0
    max_c = 0
    current_r = start[0]
    current_c = start[0]
    trenches = set()
    trenches.add(start)
    for line in data.split("\n"):
        matching = re.search(instruction_re, line)
        if matching is None:
            raise Exception
        direction, steps, color = matching.groups()
        direction = direction_map[direction]
        for _ in range(int(steps)):
            current_r += direction[0]
            current_c += direction[1]
            trenches.add((current_r, current_c))
        min_r = min(current_r, min_r)
        min_c = min(current_c, min_c)
        max_r = max(current_r, max_r)
        max_c = max(current_c, max_c)
    mapper = np.zeros((max_r - min_r + 1, max_c - min_c + 1), dtype=bool)
    for r,c in trenches:
        mapper[r-min_r,c-min_c] = True
    return binary_fill_holes(mapper).sum()

direction_map_b = {
    3:(-1,0),
    1:(1,0),
    2:(0,-1),
    0:(0,1)
}

instruction_re_b = r"[UDRL] [0-9]+ \(#([0-9a-f]{5})([0-3])\)"

def b(data):
    start = (0,0)
    current_r = start[0]
    current_c = start[0]
    min_r = 0
    min_c = 0
    edges = []
    for line in data.split("\n"):
        matching = re.search(instruction_re_b, line)
        if matching is None:
            raise Exception
        steps, direction = matching.groups()
        direction = direction_map_b[int(direction)]
        steps = int(steps, 16)
        next_r = current_r + direction[0] * steps
        next_c = current_c + direction[1] * steps
        if direction[1] != 0:
            edges.append((next_r, current_c, next_c))
        current_r, current_c = next_r, next_c
        min_r = min(current_r, min_r)
        min_c = min(current_c, min_c)
    area = 0
    for edge in edges:
        height, start_c, stop_c = edge
        height -= min_r - 1
        distance = abs(stop_c - start_c)
        length = distance + 1 if stop_c > start_c else -distance - 1
        area += height * length

    return area

year = 2023
day = 18

p = Puzzle(year=year, day=day)
data = p.input_data

example_data_a = p.examples[0].input_data
example_answer_a = p.examples[0].answer_a

#assert(a(example_data_a)==int(example_answer_a))
#assert(a(data)==35401)
#submit(a(data), part="a", year=year, day=day)

example_data_b = example_data_a
example_answer_b = 952408144115


assert(b(example_data_b)==example_answer_b)
#assert(b(data)==801)
#submit(b(data), part="b", year=year, day=day)
