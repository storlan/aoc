import numpy as np
from aocd import submit
from aocd.models import Puzzle


def a(data):
    symbol_rows = []
    numbers = []
    for r, row in enumerate(data.split("\n")):
        symbol_row = []
        number = ""
        found = False
        start = -1
        for c, val in enumerate(row):
            if val.isnumeric():
                if not found:
                    start = c
                found = True
                number += val
                symbol_row.append(False)
            elif val == ".":
                symbol_row.append(False)
                found = False
            else:
                symbol_row.append(True)
                found = False
            if len(number) > 0 and not found:
                numbers.append((int(number), start, c - 1, r))
                start = -1
                number = ""
        if len(number) > 0 and found:
            numbers.append((int(number), start, c - 1, r))

        symbol_rows.append(symbol_row)
    symbols = np.array(symbol_rows)
    sum = 0
    height, width = symbols.shape
    for val, start_c, end_c, r in numbers:
        rs = np.clip([r - 1, r + 1] , 0, height - 1)
        cs = np.clip([start_c - 1, end_c + 1], 0, width - 1)
        if symbols[rs[0]:rs[1]+1,cs[0]:cs[1]+1].sum() > 0:
            sum += val
    return sum

def add_to_gears(number, gear_map):
    val, c_start, c_end, row = number
    for r in range(max(0, row - 1), row + 2):
        for c in range(max(0, c_start - 1), c_end + 2):
            try:
                gear_map[r][c].append(val)
            except KeyError:
                continue

def b(data):
    gear_map = {}
    numbers = []
    for r, row in enumerate(data.split("\n")):
        number = ""
        found = False
        start = -1
        for c, val in enumerate(row):
            if val.isnumeric():
                if not found:
                    start = c
                found = True
                number += val

            elif val == "*":
                found = False
                if r not in gear_map:
                    gear_map[r] = {}
                gear_map[r][c] = []
            else:
                found = False
            if len(number) > 0 and not found:
                numbers.append((int(number), start, c - 1, r))
                start = -1
                number = ""
        if len(number) > 0 and found:
            numbers.append((int(number), start, c - 1, r))
    for number in numbers:
        add_to_gears(number, gear_map)
    sum = 0
    for r, gears in gear_map.items():
        for c, gear in gears.items():
            if len(gear) == 2:
                sum += gear[0] * gear[1]
    return sum


year = 2023
day = 3

p = Puzzle(year=year, day=day)
data = p.input_data

example_data_a = p.examples[0].input_data
example_answer_a = p.examples[0].answer_a

assert(a(example_data_a)==int(example_answer_a))
assert(a(data)==553825)
#submit(a(data), part="a", year=year, day=day)


example_data_b = example_data_a
example_answer_b = 467835

assert(b(example_data_b)==example_answer_b)
assert(b(data)==93994191)
#submit(b(data), part="b", year=year, day=day)
