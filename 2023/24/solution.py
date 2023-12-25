from aocd import submit
from aocd.models import Puzzle
from queue import PriorityQueue
import numpy as np
from collections import defaultdict
import re

from sympy import symbols, solve

hail_re = r"(-?[0-9]+), (-?[0-9]+), (-?[0-9]+) @ (-?[\ 0-9]+), (-?[\ 0-9]+), (-?[\ 0-9]+)"

def a(data, test_area=[200000000000000, 400000000000000]):
    start, stop = test_area
    lines = []
    for line in data.split("\n"):
        x, y, _, dx, dy, _ = [int(x) for x in re.search(hail_re, line).groups()]
        x2 = x + dx
        y2 = y + dy
        k = (y2 - y) / (x2 - x)
        m = y - k*x
        lines.append((k,m,x,dx))

    collisions = 0
    for i, (k1, m1, x_start1, x_dir1) in enumerate(lines):
        for j in range(i+1, len(lines)):
            k2, m2, x_start2, x_dir2 = lines[j]
            if j == i or k1 == k2:
                continue
            x_intersect = (m1 - m2) / (k2 - k1)
            y_intersect = k1*x_intersect + m1
            if start <= x_intersect <= stop and start <= y_intersect <= stop and np.sign(x_dir1) != np.sign(x_start1 - x_intersect) and np.sign(x_dir2) != np.sign(x_start2 - x_intersect):
                collisions += 1

    return collisions

def b(data):
    lines = []
    all_symbols = []
    equations = []
    xs, ys, zs, dxs, dys, dzs = symbols("xs ys zs dxs dys dzs") 
    for i, line in enumerate(data.split("\n")[:3]):
        lines.append([int(x) for x in re.search(hail_re, line).groups()])
        x,y,z,dx,dy,dz = [int(x) for x in re.search(hail_re, line).groups()]
        tn = symbols(f"t{i}")
        all_symbols.append(tn)
        equations.append(tn*(dx - dxs) + x - xs)
        equations.append(tn*(dy - dys) + y - ys)
        equations.append(tn*(dz - dzs) + z - zs)

    res = solve(equations)
    return res[0][xs] + res[0][ys] + res[0][zs]


year = 2023
day = 24

p = Puzzle(year=year, day=day)
data = p.input_data

example_data_a = p.examples[0].input_data
example_answer_a = 2

assert(a(example_data_a, (7,27))==int(example_answer_a))
assert(a(data)==15262)
#submit(a(data), part="a", year=year, day=day)

example_data_b = example_data_a
example_answer_b = 47

assert(b(example_data_b)==example_answer_b)
assert(b(data)==695832176624149)
#submit(b(data), part="b", year=year, day=day)
