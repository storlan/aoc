from aocd import submit
from aocd.models import Puzzle

import numpy as np
from collections import defaultdict
import random
from queue import Queue

def contract_edge(graph, merged):
    # Two random nodes
    s = random.choice(list(graph.keys()))
    t = random.choice(graph[s])
    merged[s].add(t)
    merged[s] |= merged[t]
    for node in graph[t]:
        if node != s:
            graph[s].append(node)
            graph[node].append(s)
        graph[node].remove(t)
    del graph[t]

def cut(iter_map):
    merged = defaultdict(set)
    while len(iter_map) > 2:
        contract_edge(iter_map, merged)
    cuts = len(list(iter_map.values())[0])
    return cuts, np.prod([len(merged[k]) + 1 for k in iter_map.keys()])

def a(data):
    part_map = defaultdict(list)
    for line in data.split("\n"):
        part, parts = line.split(": ")
        parts = parts.split(" ")
        for p in parts:
            part_map[p].append(part)
            part_map[part].append(p)
    prods = []
    for i in range(1000):
        cuts, prod = cut({k:v.copy() for k,v in part_map.items()})
        if cuts == 3:
            return prod
    return 0


year = 2023
day = 25

p = Puzzle(year=year, day=day)
data = p.input_data

example_data_a = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr"""
example_answer_a = 54

assert(a(example_data_a)==int(example_answer_a))
assert(a(data)==507626)
#submit(a(data), part="a", year=year, day=day)
