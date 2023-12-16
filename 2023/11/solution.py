import numpy as np
from aocd import submit
from aocd.models import Puzzle


def a(data):
    field_rows = []
    number = 0
    for line in data.split("\n"):
        new_row = []
        for col in line:
            if col == "#":
                number += 1
                new_row.append(number)
            else:
                new_row.append(0)
        field_rows.append(new_row)
    field = np.array(field_rows)
    inserted = 0
    for r,row in enumerate(field.copy()):
        if row.sum() == 0:
            field = np.insert(field, r + inserted, row, axis=0)
            inserted += 1
    inserted = 0
    dists = 0
    for c, col in enumerate(field.copy().T):
        if col.sum() == 0:
            field = np.insert(field, c + inserted, col, axis=1)
            inserted += 1
    for n1 in range(1, number+1):
        n1_coord = np.asarray(np.where(field == n1)).T[0]
        for n2 in range(n1 + 1, number + 1):
            n2_coord = np.asarray(np.where(field == n2)).T[0]
            dists += np.abs(n1_coord - n2_coord).sum()
    return dists

def add_millions(r_range, c_range, empty_rows, empty_cols, multiplier=1000000):
    addage = 0
    for r in r_range:
        if r in empty_rows:
            addage += multiplier - 1
    for c in c_range:
        if c in empty_cols:
            addage += multiplier - 1
    return addage

def b(data, multiplier=1000000):
    field_rows = []
    number = 0
    for line in data.split("\n"):
        new_row = []
        for col in line:
            if col == "#":
                number += 1
                new_row.append(number)
            else:
                new_row.append(0)
        field_rows.append(new_row)
    field = np.array(field_rows)
    empty_rows = set()
    for r, row in enumerate(field.copy()):
        if row.sum() == 0:
            empty_rows.add(r)
    empty_cols = set()
    for c, col in enumerate(field.copy().T):
        if col.sum() == 0:
            empty_cols.add(c)
    dists = 0
    for n1 in range(1, number + 1):
        n1_coord = np.asarray(np.where(field == n1)).T[0]
        for n2 in range(n1 + 1, number + 1):
            n2_coord = np.asarray(np.where(field == n2)).T[0]
            dists += np.abs(n1_coord - n2_coord).sum() + add_millions(r_range=np.arange(min(n1_coord[0], n2_coord[0]), max(n1_coord[0], n2_coord[0]) + 1), c_range=np.arange(min(n1_coord[1], n2_coord[1]), max(n1_coord[1], n2_coord[1]) + 1), empty_rows=empty_rows, empty_cols=empty_cols, multiplier=multiplier)
    return dists

year = 2023
day = 11

p = Puzzle(year=year, day=day)
data = p.input_data

example_data_a = p.examples[0].input_data
example_answer_a = p.examples[0].answer_a


assert(a(example_data_a)==int(example_answer_a))
assert(a(data)==10077850)
# submit(a(data), part="a", year=year, day=day)


example_data_b = example_data_a
example_answer_b = 1030
example_multiplier = 10

assert(b(example_data_b, example_multiplier)==example_answer_b)

example_answer_b = 8410
example_multiplier = 100

assert(b(example_data_b, example_multiplier)==example_answer_b)
assert(b(data)==504715068438)
# submit(b(data), part="b", year=year, day=day)
