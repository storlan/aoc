from aocd import submit
from aocd.models import Puzzle

from scipy.ndimage import binary_fill_holes
import numpy as np
import re


instruction_re = r"([UDRL]) ([0-9]+) \(#[0-9a-f]+\)"


direction_map = {
    "U":(-1,0),
    "D":(1,0),
    "L":(0,-1),
    "R":(0,1)
}

def get_steps_and_direction(line):
    matching = re.search(instruction_re, line)
    if matching is None:
        raise Exception
    direction, steps = matching.groups()
    direction = direction_map[direction]
    return int(steps), direction

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
        steps, direction = get_steps_and_direction(line)
        for _ in range(steps):
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


def get_steps_and_direction_b(line):
    matching = re.search(instruction_re_b, line)
    if matching is None:
        raise Exception
    steps, direction = matching.groups()
    direction = direction_map_b[int(direction)]
    steps = int(steps, 16)
    return steps, direction


def b(data):
    lines = data.split("\n")
    _, prev_direction = get_steps_and_direction_b(lines[-1])
    start = (0,0)
    current_r = start[0]
    current_c = start[0]
    min_r = 0
    corners = []
    for line in lines:
        steps, direction = get_steps_and_direction_b(line)
        next_r = current_r + direction[0] * steps
        next_c = current_c + direction[1] * steps
        combination = (direction[0] + prev_direction[0], direction[1] + prev_direction[1])
        if combination[1] > 0:
            height_adjust = -0.5
        else:
            height_adjust = 0.5
        if combination[0] > 0:
            col_adjust = 0.5
        else:
            col_adjust = -0.5
        corners.append((current_r + height_adjust, current_c + col_adjust))
        current_r, current_c = next_r, next_c
        prev_direction = direction
        min_r = min(current_r, min_r)
   
    area = 0
    old = corners[0]
    for i in range(1, len(corners) + 1):
        new = corners[i % len(corners)]
        length = new[1] - old[1]
        if length == 0:
            continue
        area += (new[0] - (min_r - 1)) * length
        old = new


    return int(abs(area))


year = 2023
day = 18


p = Puzzle(year=year, day=day)
data = p.input_data


example_data_a = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""
example_answer_a = 62


assert(a(example_data_a)==example_answer_a)
assert(a(data)==35401)
#submit(a(data), part="a", year=year, day=day)


example_data_b = example_data_a
example_answer_b = 952408144115




assert(b(example_data_b)==example_answer_b)
assert(b(data)==48020869073824)
#submit(b(data), part="b", year=year, day=day)
