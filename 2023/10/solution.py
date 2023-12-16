import numpy as np
from aocd import submit
from aocd.models import Puzzle

from queue import PriorityQueue, Queue

pipes = {
    "|":((1,0),(-1,0)),
    "-":((0,1),(0,-1)),
    "L":((-1,0),(0,1)),
    "J":((-1,0),(0,-1)),
    "7":((1,0),(0,-1)),
    "F":((1,0),(0,1)),
}

def djikstra(neighbors, start):
    costs = {key:np.inf for key in neighbors.keys()}
    costs[start[0],start[1]] = 0
    visited = set()
    q = PriorityQueue()
    q.put((0, (start[0], start[1])))
    while True:
        if q.empty():
            break
        current_cost, current = q.get()
        for r, c in neighbors[current]:
            tentative_cost = current_cost + 1
            if tentative_cost < costs[r,c]:
                costs[r,c] = tentative_cost
            if current not in visited :
                new_item = (costs[r,c], (r, c))
                if new_item not in q.queue:
                    q.put((costs[r,c], (r, c)))
        visited.add(current)

    visited_costs = [costs[x] for x in visited]
    return np.max(visited_costs), visited

def a(data):
    start = (-1,-1)
    neighbors = {}
    for r, row in enumerate(data.split("\n")):
        for c, col in enumerate(row):
            if col == "S":
                start = (r, c)
                continue
            elif col in pipes:
                connection = pipes[col]
                neighbors[r,c] = [(r + connection[0][0], c + connection[0][1]), (r + connection[1][0], c + connection[1][1])]
    if start == (-1, -1):
        raise Exception
    neighbors[start[0],start[1]] = []
    for key, ns in neighbors.items():
        for n in ns:
            if n == start:
                neighbors[start[0],start[1]].append(key)
    max_cost, _ = djikstra(neighbors, start)
    return max_cost

friends = [(1,0),(-1,0),(0,1),(0,-1)]

def can_escape(coord, escaped, no_escape, loop_coords):
    height, width = loop_coords.shape
    q = Queue()
    queued = set()
    q.put(coord)
    queued.add(coord)
    visited = np.zeros((height, width)).astype(bool)
    while not q.empty():
        current_r, current_c = q.get()
        queued.remove((current_r, current_c))
        visited[current_r, current_c] = True
        for r_add, c_add in friends:
            r_new, c_new = current_r + r_add, current_c + c_add
            if loop_coords[r_new, c_new]:
                continue
            if escaped[r_new, c_new] or r_new <= 0 or c_new <= 0 or r_new >= height - 1 or c_new >= width - 1:
                visited[r_new, c_new] = True
                return True, visited
            if not visited[r_new, c_new] and (r_new, c_new) not in queued:
                q.put((r_new, c_new))
                queued.add((r_new, c_new))
    return False, visited


def b(data):
    start = (-1, -1)
    neighbors = {}
    empties = set()
    for r, row in enumerate(data.split("\n")):
        for c, col in enumerate(row):
            if col == "S":
                start = (r, c)
                continue
            elif col in pipes:
                connection = pipes[col]
                neighbors[r, c] = [(r + connection[0][0], c + connection[0][1]),
                                   (r + connection[1][0], c + connection[1][1])]
            else:
                empties.add((r,c))
    width = c + 1
    height = r + 1
    if start == (-1, -1):
        raise Exception
    neighbors[start] = []
    for key, ns in neighbors.items():
        for n in ns:
            if n == start:
                neighbors[start].append(key)
    current_coord = start
    next_coord = neighbors[start][0]
    diff = np.array((next_coord[0] - current_coord[0], next_coord[1] - current_coord[1]))
    loop_map = np.zeros((height * 2, width * 2)).astype(bool)
    loop_map[start[0]*2, start[1]*2] = True
    loop_map[start[0] * 2 + diff[0], start[1] * 2 + diff[1]] = True
    while next_coord != start:
        current_coord, next_coord = next_coord, [x for x in neighbors[next_coord] if x != current_coord][0]
        diff = (next_coord[0] - current_coord[0], next_coord[1] - current_coord[1])
        loop_map[current_coord[0] * 2, current_coord[1] * 2] = True
        loop_map[current_coord[0] * 2 + diff[0], current_coord[1] * 2 + diff[1]] = True
    for r,c in neighbors.keys():
        if not loop_map[r*2,c*2]:
            empties.add((r,c))

    escaped = np.zeros((height * 2, width * 2)).astype(bool)
    no_escape = np.zeros((height * 2, width * 2)).astype(bool)
    counter = 0
    i = 0
    for empty in empties:
        up_coord = empty[0]*2, empty[1]*2
        res, visited = can_escape(up_coord, escaped, no_escape, loop_map)
        if not res:
            counter += 1
            no_escape = np.logical_or(no_escape, visited)
        else:
            escaped = np.logical_or(escaped, visited)
        i += 1
    return counter

year = 2023
day = 10

p = Puzzle(year=year, day=day)
data = p.input_data

example_data_a = """.....
.S-7.
.|.|.
.L-J.
....."""
example_answer_a = 4
example_data_a_2 ="""..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""
example_answer_a_2 = 8



assert(a(example_data_a)==example_answer_a)
assert(a(example_data_a_2)==example_answer_a_2)
assert(a(data)==6812)
# submit(a(data), part="a", year=year, day=day)


example_data_b = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""
example_answer_b = 4
example_data_b_2 = """..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
.........."""
example_answer_b_2 = 4
example_data_b_3 = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""
example_answer_b_3 = 8

example_data_b_4 = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJIF7FJ-
L---JF-JLJIIIIFJLJJ7
|F|F-JF---7IIIL7L|7|
|FFJF7L7F-JF7IIL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""
example_answer_b_4 = 10

assert(b(example_data_b)==example_answer_b)
assert(b(example_data_b_2)==example_answer_b_2)
assert(b(example_data_b_3)==example_answer_b_3)
assert(b(example_data_b_4)==example_answer_b_4)
assert(b(data)==527)
# submit(b(data), part="b", year=year, day=day)
