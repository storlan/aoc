from aocd import submit
from aocd.models import Puzzle
import re
import numpy as np

def follow_instructions(item, all_instructions):
    current = "in"
    while True:
        if current == "A":
            return True
        elif current == "R":
            return False
        instructions = all_instructions[current]
        found = False
        for inst in instructions[:-1]:
            var_name, operator, val, dest = inst
            item_val = item[var_name]
            if operator == "<" and item_val < val:
                current = dest
                found = True
                break
            elif operator == ">" and item_val > val:
                current = dest
                found = True
                break
        if not found:
            current = instructions[-1]


def a(data):
    data1, data2 = data.split("\n\n")
    all_instructions = {}
    for line in data1.split("\n"):
        name, instructions = line.split("{")
        all_instructions[name] = []
        instructions = instructions[:-1].split(",")
        for inst in instructions[:-1]:
            condition, dest = inst.split(":")
            var_name, operator, val = re.split(r"([<>])", condition)
            all_instructions[name].append((var_name, operator, int(val), dest))
        all_instructions[name].append(instructions[-1])

    items = []
    sum = 0
    for line in data2.split("\n"):
        attributes = line[1:-1].split(",")
        item = {}
        for attribute in attributes:
            name, val = attribute.split("=")
            item[name] = int(val)
        items.append(item)
        if follow_instructions(item, all_instructions):
            sum += np.sum(list(item.values()))
    return sum


def explore_path(current_label, bounds, accepted_paths, all_instructions, labels):
    if current_label == "A":
        accepted_paths.append(bounds)
        return
    elif current_label == "R":
        return
    instructions = all_instructions[current_label]
    default_label = instructions[-1]
    default_case_bounds = {k:v.copy() for k, v in bounds.items()}
    instructions = instructions[:-1]
    for instruction in instructions:
        var_name, operator, val, dest = instruction
        new_bounds = {k:v.copy() for k, v in default_case_bounds.items()}
        if operator == "<":
            new_bounds[var_name][1] = min(new_bounds[var_name][1], val - 1)
            default_case_bounds[var_name][0] = max(default_case_bounds[var_name][0], val)
        elif operator == ">":
            new_bounds[var_name][0] = max(new_bounds[var_name][0], val + 1)
            default_case_bounds[var_name][1] = min(default_case_bounds[var_name][1], val)
        explore_path(dest, new_bounds, accepted_paths, all_instructions, labels + [dest])
    explore_path(default_label, default_case_bounds, accepted_paths, all_instructions, labels + [default_label])


def follow_instructions_b(all_instructions):
    default_bounds = {
        "x":[1,4000],
        "m":[1,4000],
        "a":[1,4000],
        "s":[1,4000]
    }
    accepted_paths = []
    explore_path("in", default_bounds, accepted_paths, all_instructions, ["in"])
    sum = 0
    for path in accepted_paths:
        possibilities = 1
        for start, stop in path.values():
            possibilities *= (stop - start) + 1
        sum += possibilities
    return sum


def b(data):
    lines = data.split("\n\n")[0].split("\n")
    all_instructions = {}
    for line in lines:
        name, instructions = line.split("{")
        all_instructions[name] = []
        instructions = instructions[:-1].split(",")
        for inst in instructions[:-1]:
            condition, dest = inst.split(":")
            var_name, operator, val = re.split(r"([<>])", condition)
            all_instructions[name].append((var_name, operator, int(val), dest))
        all_instructions[name].append(instructions[-1])

    return follow_instructions_b(all_instructions)




year = 2023
day = 19


p = Puzzle(year=year, day=day)
data = p.input_data


example_data_a = p.examples[0].input_data
example_answer_a = p.examples[0].answer_a


assert(a(example_data_a)==int(example_answer_a))
assert(a(data)==398527)
#submit(a(data), part="a", year=year, day=day)


example_data_b = example_data_a
example_answer_b = 167409079868000


assert(b(example_data_b)==example_answer_b)
assert(b(data)==133973513090020)
#submit(b(data), part="b", year=year, day=day)
