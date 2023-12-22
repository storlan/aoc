from aocd import submit
from aocd.models import Puzzle
import re
import numpy as np

def fall_down(brick, coord_to_brick_map, support_map, rest_map):
    coords = []
    start, stop, name = brick
    
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
                    support_map[impact] = []
                support_map[impact].append(name)
                rest_map[name] = impacts
            break
        min_z -= 1
        coords = new_coords
    for coord in coords:
        coord_to_brick_map[coord] = name
    

def a(data):
    bricks = []
    for i, line in enumerate(data.split("\n")):
        start, stop = line.split("~")
        start = tuple(int(x) for x in start.split(","))
        stop = tuple(int(x) for x in stop.split(","))
        bricks.append((start,stop,i))
    bricks.sort(key=lambda x: x[0][2])

    support_map = {}
    rest_map = {}
    coord_to_brick_map = {}
    for brick in bricks:
        fall_down(brick, coord_to_brick_map, support_map, rest_map)
    res = 0
    for i in range(len(bricks)):
        if i not in support_map:
            res += 1
            continue
        for supported in support_map[i]:
            if len(rest_map[supported]) > 1:
                res += 1
                break
    
    return res

def b(data):
    
    return 0




year = 2023
day = 22


p = Puzzle(year=year, day=day)
data = p.input_data


example_data_a = p.examples[0].input_data
example_answer_a = p.examples[0].answer_a


#assert(a(example_data_a)==int(example_answer_a))
assert(a(data)!=538)
#submit(a(data), part="a", year=year, day=day)


#example_data_b = example_data_a
#example_answer_b = 167409079868000


#assert(b(example_data_b)==example_answer_b)
#assert(b(data)==133973513090020)
#submit(b(data), part="b", year=year, day=day)
