from aocd import submit
from aocd.models import Puzzle
from queue import PriorityQueue
import numpy as np
from collections import defaultdict


dir_map = {
    (1,0):[(0,-1),(0,1)],
    (-1,0):[(0,-1),(0,1)],
    (0,1):[(1,0),(-1,0)],
    (0,-1):[(1,0),(-1,0)],
}

arrow_map = {
    ">":(0,1),
    "^":(-1,0),
    "v":(1,0),
    "<":(0,-1)
}

directions = [(1,0),(-1,0),(0,1),(0,-1)]

def bad_coord(coord, forrests):
    r,c = coord
    height, width = forrests.shape
    return r < 0 or c < 0 or r == height or c == width or forrests[coord]

def check_direction(r, c, r_dir, c_dir, current_cost, forrests, slopes, q, costs, path):
    r_new = r + r_dir
    c_new = c + c_dir
    new_entry = (r_new, c_new)
    if bad_coord(new_entry, forrests) or new_entry in path:
        return
    cost = 1 + current_cost
    new_path = path.copy()
    if new_entry in slopes:
        slide_r, slide_c = slopes[new_entry]
        new_entry = (slide_r + r_new, slide_c + c_new)
        if new_entry in path or cost < costs[(r_new, c_new)]:
            return
        costs[(r_new, c_new)] = cost
        new_path.add((r_new, c_new))
        cost += 1
        
    if cost < costs[new_entry]:
        return
    if cost > costs[new_entry]:
        costs[new_entry] = cost
    new_path.add(new_entry)
    q.put((cost, new_entry, new_path))


def djikstra(start, end, forrests, slopes):
    costs = np.zeros(forrests.shape, dtype=int)
    costs[start] = 0
    path = set([start])
    q = PriorityQueue()
    q.put((0, start, path))
    while not q.empty():
        current_cost, (r, c), path = q.get()
        # if (r,c) == end:
        #     break
        for r_dir, c_dir in directions:
            check_direction(r, c, r_dir, c_dir, current_cost, forrests, slopes, q, costs, path)
    return costs[end]

def a(data):
    forrests = []
    slopes = {}
    for r,row in enumerate(data.split("\n")):
        forrest_row = []
        for c, char in enumerate(row):
            if char == "#":
                forrest_row.append(True)
            elif char in arrow_map:
                slopes[r,c] = arrow_map[char]
                forrest_row.append(False)
            else:
                forrest_row.append(False)
        forrests.append(forrest_row)
    forrests = np.array(forrests, dtype=bool)
    h,w = forrests.shape
    return int(djikstra((0,1), (h-1, w-2), forrests, slopes))

def find_node_connections(start, node_for_coord, forrests):
    q = PriorityQueue()
    q.put((0, start, set([start])))
    connections = []
    while not q.empty():
        current_cost, (r, c), path = q.get()
        for r_dir, c_dir in directions:
            new_coord = (r + r_dir, c+ c_dir)
            if bad_coord(new_coord, forrests) or new_coord in path:
                continue
            if new_coord in node_for_coord:
                connections.append((node_for_coord[new_coord], current_cost + 1))
                continue
            new_path = path.copy()
            new_path.add(new_coord)
            q.put((current_cost + 1, new_coord, new_path))
    return connections

def find_longest_path(node, path, end_node, cost, connection_map, biggest_cost):
    if node == end_node:
        return cost
    for next_node, next_cost in connection_map[node]:
        if not next_node in path:
            new_path = path.copy()
            new_path.add(next_node)
            biggest_cost = max(biggest_cost, find_longest_path(next_node, new_path, end_node, cost + next_cost, connection_map, biggest_cost))
    return biggest_cost

def b(data):
    forrests = []
    node_candidates = defaultdict(int)
    for r,row in enumerate(data.split("\n")):
        forrest_row = []
        for c, char in enumerate(row):
            if char == "#":
                forrest_row.append(True)
            elif char in arrow_map:
                a_r, a_c = arrow_map[char]
                node_candidates[(r + a_r, c + a_c)] += 1
                node_candidates[(r - a_r, c - a_c)] += 1
                forrest_row.append(False)
            else:
                forrest_row.append(False)
        forrests.append(forrest_row)
    coord_of_node = {0:(0,1)}
    node_for_coord = {(0,1):0}
    i = 1
    for (r,c), count in node_candidates.items():
        if count >= 3:
            coord_of_node[i] = (r, c)
            node_for_coord[(r, c)] = i
            i += 1
    end_node = i
    forrests = np.array(forrests, dtype=bool)
    h,w = forrests.shape
    coord_of_node[end_node] = (h-1, w-2)
    node_for_coord[(h-1, w-2)] = end_node
    connection_map = {name:find_node_connections(coord, node_for_coord, forrests) for name, coord in coord_of_node.items()}
    
    return find_longest_path(0, set(), end_node, 0, connection_map, 0)

year = 2023
day = 23

p = Puzzle(year=year, day=day)
data = p.input_data

example_data_a = p.examples[0].input_data
example_answer_a = 94

assert(a(example_data_a)==int(example_answer_a))
assert(a(data)==2018)
#submit(a(data), part="a", year=year, day=day)

example_data_b = example_data_a
example_answer_b = 154


assert(b(example_data_b)==example_answer_b)
assert(b(data)==6406)
#submit(b(data), part="b", year=year, day=day)
