import numpy as np
from aocd import submit
from aocd.models import Puzzle

def tilt_rocks(rocks, stops):
    i = 0
    for rock_row, stop_row in zip(rocks, stops):
        new_rock_row = np.zeros(rock_row.shape, dtype=bool)
        for rock in np.where(rock_row)[0]:
            max_pos = 0
            row_stops = np.argwhere(stop_row[:rock])
            if len(row_stops) > 0:
                max_pos = np.max(row_stops) + 1
            new_rock_stops = np.argwhere(new_rock_row[:rock])
            if len(new_rock_stops) > 0:
                max_pos = max(np.max(new_rock_stops) + 1, max_pos)
            new_rock_row[max_pos] = True
        rocks[i,:] = new_rock_row
        i += 1
    return rocks

def a(data):
    rocks = []
    stops = []
    for line in data.split("\n"):
        stops.append([c == "#" for c in line])
        rocks.append([c == "O" for c in line])
    rocks = np.array(rocks)
    stops = np.array(stops)

    sum = 0
    i = 0
    for rock_col, stop_col in zip(rocks.T, stops.T):
        new_rock_col = np.zeros(rock_col.shape, dtype=bool)
        for rock in np.where(rock_col)[0]:
            max_pos = 0
            col_stops = np.argwhere(stop_col[:rock])
            if len(col_stops) > 0:
                max_pos = np.max(col_stops) + 1
            new_rock_stops = np.argwhere(new_rock_col[:rock])
            if len(new_rock_stops) > 0:
                max_pos = max(np.max(new_rock_stops) + 1, max_pos)
            new_rock_col[max_pos] = True
        rocks[:,i] = new_rock_col
        i += 1
    height = rocks.shape[0]
    for i, row in enumerate(rocks):
        sum += np.sum(row) * (height - i)
    return sum

def b(data):
    rocks = []
    stops = []
    for line in data.split("\n"):
        stops.append([c == "#" for c in line])
        rocks.append([c == "O" for c in line])
    rocks = np.array(rocks)
    stops = np.array(stops)

    rocks = np.rot90(rocks)
    stops = np.rot90(stops)
    sums_to_sequence = {}

    found = False
    sum_list = []
    for j in range(1000000000):
        for _ in range(4):
            rocks = tilt_rocks(rocks, stops)
            rocks = np.rot90(rocks, -1)
            stops = np.rot90(stops, -1)
        sum = 0
        height = rocks.shape[1]
        for i, row in enumerate(rocks.T):
            sum += np.sum(row) * (height - i)

        if sum not in sums_to_sequence:
            sums_to_sequence[sum] = []
        if j > 4:
            sums_to_sequence[sum].append((j, tuple(sum_list[-4:])))
        sum_list.append(sum)
        if len(sums_to_sequence[sum]) >= 3:
            i_latest, seq_latest = sums_to_sequence[sum][-1]
            i_old, seq_old = sums_to_sequence[sum][-2]
            if seq_old == seq_latest:
                found = True
                period = i_latest - i_old
        if found and 1000000000 % period == (j+1) % period:
            break

    return sum

year = 2023
day = 14

p = Puzzle(year=year, day=day)
data = p.input_data

example_data_a = p.examples[0].input_data
example_answer_a = p.examples[0].answer_a

assert(a(example_data_a)==int(example_answer_a))
assert(a(data)==110274)
#submit(a(data), part="a", year=year, day=day)

example_data_b = example_data_a
example_answer_b = 64

assert(b(example_data_b)==example_answer_b)
assert(b(data)==90982)
#submit(b(data), part="b", year=year, day=day)
