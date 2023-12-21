from aocd import submit
from aocd.models import Puzzle

import numpy as np

import matplotlib.pyplot as plt

neighbors = [(1,0),(-1,0),(0,1),(0,-1)]

def inside(r,c, height, width):
    return r >= 0 and c >= 0 and r < height and c < width

def a(data, steps=64):
    data_rows = []
    start = None
    for r, line in enumerate(data.split("\n")):
        if start is None and "S" in line:
            c = line.index("S")
            start = (r,c)
        data_rows.append([x != "#" for x in line])
    gardens = np.array(data_rows, dtype=bool)
    height, width = gardens.shape
    current_positions = set([start])
    for step in range(1, steps + 1):
        next_positions = set()
        for r, c in current_positions:
            for r_add, c_add in neighbors:
                r_new, c_new = r + r_add, c + c_add
                if inside(r_new, c_new, height, width) and gardens[r_new, c_new]:
                    next_positions.add((r_new, c_new))
        current_positions = next_positions

    return len(current_positions)



def b(data, steps=26501365):
    data_rows = []
    start = None
    for r, line in enumerate(data.split("\n")):
        if start is None and "S" in line:
            c = line.index("S")
            start = (r,c)
        data_rows.append([x != "#" for x in line])
    gardens = np.array(data_rows, dtype=bool)
    height, width = gardens.shape
    visited = set([(start[0], start[1])])
    visit_count = 1
    current_positions = set([start])
    for step in range(1, steps + 1):
        next_positions = set()
        new_visited = set()
        for r, c in current_positions:
            for r_add, c_add in neighbors:
                r_new, c_new = r + r_add, c + c_add
                if gardens[r_new % height, c_new % width] and (r_new, c_new) not in visited:
                    next_positions.add((r_new, c_new))
                    visited.add((r_new, c_new))
                    new_visited.add((r_new, c_new))
                    if step % 2 == 0:
                        visit_count += 1
        if step + 1 % 2 == 0:
            visited = new_visited
        current_positions = next_positions
    return visit_count


year = 2023
day = 21


p = Puzzle(year=year, day=day)
data = p.input_data


example_data_a = p.examples[0].input_data
example_answer_a = 16


#assert(a(example_data_a, 6)==int(example_answer_a))
#assert(a(data)==3687)
#submit(a(data), part="a", year=year, day=day)


example_data_b = example_data_a
example_answer_b = 16
steps = 6
assert(b(example_data_b, steps)==example_answer_b)

example_answer_b = 50
steps = 10
assert(b(example_data_b, steps)==example_answer_b)

example_answer_b = 1594
steps = 50
assert(b(example_data_b, steps)==example_answer_b)

example_answer_b = 6536
steps = 100
assert(b(example_data_b, steps)==example_answer_b)

example_answer_b = 167004
steps = 500
assert(b(example_data_b, steps)==example_answer_b)

example_answer_b = 668697
steps = 1000
assert(b(example_data_b, steps)==example_answer_b)

example_answer_b = 16733044
steps = 5000
assert(b(example_data_b, steps)==example_answer_b)

# assert(b(data)==48020869073824)
#submit(b(data), part="b", year=year, day=day)
