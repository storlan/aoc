import numpy as np
from aocd import submit
from aocd.models import Puzzle

def find_reflection(map):
    height = map.shape[0]
    for i in range(height - 1):
        if np.array_equal(map[i,:], map[i+1,:]):
            ok = True
            for j in range(min(i+1, height - i - 1)):
                if not np.array_equal(map[i-j,:], map[i+1+j,:]):
                    ok = False
                    break
            if ok:
                return i
    return -1

def smudge_reflection(map):
    height, width = map.shape
    smudge_not_found = True
    for i in range(height - 1):
        equalness = np.sum([map[i,x] == map[i+1, x] for x in range(width)])
        if smudge_not_found and equalness == width - 1:
            smudge_not_found = False
            equal = True
        else:
            equal = equalness == width
        if equal:
            ok = True
            for j in range(1,min(i+1, height - i - 1)):
                equalness = np.sum([map[i-j,x] == map[i+1+j, x] for x in range(width)])
                if smudge_not_found and equalness == width - 1:
                    smudge_not_found = False
                    equal = True
                else:
                    equal = equalness == width
                if not equal:
                    ok = False
                    break
            if ok and not smudge_not_found:
                return i
        smudge_not_found = True
    return -1

def a(data):
    row_data = []
    all_data = []
    for line in data.split("\n"):
        if len(line) == 0:
            all_data.append(np.array(row_data))
            row_data = []
            continue
        row_data.append([c == "#" for c in line])
    all_data.append(np.array(row_data))
    sum = 0
    for map in all_data:
        row_index = find_reflection(map)
        col_index = find_reflection(map.T)
        res = col_index + 1 + 100 * (row_index + 1)
        sum += res
    return sum

def b(data):
    row_data = []
    all_data = []
    for line in data.split("\n"):
        if len(line) == 0:
            all_data.append(np.array(row_data))
            row_data = []
            continue
        row_data.append([c == "#" for c in line])
    all_data.append(np.array(row_data))
    sum = 0
    for map in all_data:
        if sum == 2207:
            print()
        row_index = smudge_reflection(map)
        col_index = smudge_reflection(map.T)
        res = col_index + 1 + 100 * (row_index + 1)
        sum += res
    return sum

year = 2023
day = 13

p = Puzzle(year=year, day=day)
data = p.input_data

example_data_a = p.examples[0].input_data
example_answer_a = p.examples[0].answer_a

assert(a(example_data_a)==int(example_answer_a))
assert(a(data)==37025)
# submit(a(data), part="a", year=year, day=day)

example_data_b = example_data_a
example_answer_b = 400

assert(b(example_data_b)==example_answer_b)
assert(b(data)==32854)
# submit(b(data), part="b", year=year, day=day)
