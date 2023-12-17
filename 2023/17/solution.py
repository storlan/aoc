from aocd import submit
from aocd.models import Puzzle
from queue import PriorityQueue
import numpy as np

dir_map = {
    (1,0):[(0,-1),(0,1)],
    (-1,0):[(0,-1),(0,1)],
    (0,1):[(1,0),(-1,0)],
    (0,-1):[(1,0),(-1,0)],
}

def not_valid_neighbor(r, c, height, width):
    return r < 0 or c < 0 or r >= height or c >= width

def check_direction(r, c, r_dir_new, c_dir_new, current_cost, straights, tiles, visited, q, costs, end, path):
    r_new = r + r_dir_new
    c_new = c + c_dir_new
    
    height, width = tiles.shape
    if not_valid_neighbor(r_new, c_new, height, width):
        return
    cost = tiles[r_new, c_new] + current_cost
    new_entry = (r_new, c_new, r_dir_new, c_dir_new, straights)
    if new_entry in visited and cost > costs[r_new, c_new]:
        return
    if cost < costs[r_new, c_new]:
        costs[r_new, c_new] = cost
    dist = end[0] - r_new + end[1] - c_new
    visited.add((r_new, c_new, r_dir_new, c_dir_new, straights))
    q.put((cost + dist, (r_new, c_new, r_dir_new, c_dir_new, straights, cost), path + [(r_new, c_new)]))


def astar(tiles, start, end):
    costs = np.ones(tiles.shape) * np.inf
    costs[start[0], start[1]] = 0
    visited = set()
    q = PriorityQueue()
    q.put((0, (start[0], start[1], 0, 1, -1, 0), [(0,0)]))
    q.put((0, (start[0], start[1], 1, 0, -1, 0), [(0,0)]))
    visited = set()
    while not q.empty():
        _, (r, c, r_dir, c_dir, straights, current_cost), path = q.get()
        if (r,c) == end:
            break
        for r_dir_new, c_dir_new in dir_map[(r_dir, c_dir)]:
            check_direction(r, c, r_dir_new, c_dir_new, current_cost, 0, tiles, visited, q, costs, end, path)
        if straights < 2:
            check_direction(r, c, r_dir, c_dir, current_cost, straights + 1, tiles, visited, q, costs, end, path)
    return costs[end[0], end[1]]

def astar_b(tiles, start, end):
    costs = np.ones(tiles.shape) * np.inf
    costs[start[0], start[1]] = 0
    visited = set()
    q = PriorityQueue()
    q.put((0, (start[0], start[1], 0, 1, -1, 0), [(0,0)]))
    q.put((0, (start[0], start[1], 1, 0, -1, 0), [(0,0)]))
    visited = set()
    height, width = costs.shape
    while not q.empty():
        _, (r, c, r_dir, c_dir, straights, current_cost), path = q.get()
        if (r,c) == end:
            break
        if straights >= 3:
            for r_dir_new, c_dir_new in dir_map[(r_dir, c_dir)]:
                if not not_valid_neighbor(r + r_dir_new * 4, c + c_dir_new * 4, height, width):
                    check_direction(r, c, r_dir_new, c_dir_new, current_cost, 0, tiles, visited, q, costs, end, path)
        if straights < 9:
            check_direction(r, c, r_dir, c_dir, current_cost, straights + 1, tiles, visited, q, costs, end, path)
    return costs[end[0], end[1]]

def a(data):
    data = np.array([list(line) for line in data.split("\n")], dtype=int)
    h,w = data.shape
    return int(astar(data, (0,0), (h-1, w-1)))

def b(data):
    data = np.array([list(line) for line in data.split("\n")], dtype=int)
    h,w = data.shape
    return int(astar_b(data, (0,0), (h-1, w-1)))

year = 2023
day = 17

p = Puzzle(year=year, day=day)
data = p.input_data

example_data_a = p.examples[0].input_data
example_answer_a = p.examples[0].answer_a

assert(a(example_data_a)==int(example_answer_a))
assert(a(data)==686)
#submit(a(data), part="a", year=year, day=day)

example_data_b = example_data_a
example_answer_b = 94

example_data_b_2 = """111111111111
999999999991
999999999991
999999999991
999999999991"""
example_answer_b_2 = 71

assert(b(example_data_b)==example_answer_b)
assert(b(example_data_b_2)==example_answer_b_2)
assert(b(data)==801)
#submit(b(data), part="b", year=year, day=day)
