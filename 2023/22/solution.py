from aocd import submit
from aocd.models import Puzzle
import numpy as np


def fall_down(brick, name, coord_to_brick_map, support_map, rest_map, debug):
    coords = []
    start, stop = brick
    min_z = np.inf
    for x in range(start[0], stop[0]+1):
            for y in range(start[1], stop[1]+1):
                for z in range(start[2], stop[2]+1):
                    coords.append((x,y,z))
                    min_z = min(min_z, z)
    while min_z > 1:
        impacts = set()
        new_coords = []
        for x,y,z in coords:
            new_coord = (x,y,z-1)
            if new_coord in coord_to_brick_map:
                impacts.add(coord_to_brick_map[new_coord])
            else:
                new_coords.append((new_coord))
        if len(impacts) > 0:
            for impact in impacts:
                if impact not in support_map:
                    support_map[impact] = set()
                if name in support_map[impact]:
                    print()
                support_map[impact].add(name)
            if name in rest_map:
                print()
            rest_map[name] = impacts
            break
        min_z -= 1
        coords = new_coords

    for coord in coords:
        coord_to_brick_map[coord] = name
        debug[coord[0], coord[1], coord[2]] = name

def a(data):
    bricks = []
    for i, line in enumerate(data.split("\n")):
        start, stop = line.split("~")
        start = tuple(int(x) for x in start.split(","))
        stop = tuple(int(x) for x in stop.split(","))
        bricks.append((start,stop))
    bricks.sort(key=lambda x: x[0][2])

    support_map = {}
    rest_map = {}
    coord_to_brick_map = {}
    debug = np.zeros((10,10,200))
    for name, brick in enumerate(bricks):
        fall_down(brick, name+1, coord_to_brick_map, support_map, rest_map, debug)
    res = 0
    for i in range(1, len(bricks) + 1):
        if i not in support_map:
            res += 1
            continue
        ok = True
        for supported in support_map[i]:
            if len(rest_map[supported]) <= 1:
                ok = False
                break
        if ok:
            res += 1
    return res

def support_chain(name, rest_map, support_map, names):
    if name not in support_map:
        names.add(name)
        return
    next_gen = []
    for n in support_map[name]:
        if all([n1 in names for n1 in rest_map[n]]):
            names.add(n)
            next_gen.append(n)
    for n in next_gen:
        support_chain(n, rest_map, support_map, names)
    return

def b(data):
    bricks = []
    for i, line in enumerate(data.split("\n")):
        start, stop = line.split("~")
        start = tuple(int(x) for x in start.split(","))
        stop = tuple(int(x) for x in stop.split(","))
        bricks.append((start,stop))
    bricks.sort(key=lambda x: x[0][2])

    support_map = {}
    rest_map = {}
    coord_to_brick_map = {}
    debug = np.zeros((10,10,200))
    for name, brick in enumerate(bricks):
        fall_down(brick, name+1, coord_to_brick_map, support_map, rest_map, debug)
    res = 0
    for i in range(1, len(bricks) + 1):
        if i not in support_map:
            continue
        for supported in support_map[i]:
            if len(rest_map[supported]) <= 1:
                fall_names = set([i])
                support_chain(i, rest_map, support_map, fall_names)
                res += len(fall_names) - 1
                break

    return res




year = 2023
day = 22


p = Puzzle(year=year, day=day)
data = p.input_data


example_data_a = p.examples[0].input_data
example_answer_a = p.examples[0].answer_a


assert(a(example_data_a)==int(example_answer_a))
assert(a(data)==446)
# submit(a(data), part="a", year=year, day=day)


example_data_b = example_data_a
example_answer_b = 7


assert(b(example_data_b)==example_answer_b)
assert(b(data)==60287)
#submit(b(data), part="b", year=year, day=day)
