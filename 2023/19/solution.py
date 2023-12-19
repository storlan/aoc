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
        


    pass

def a(data):
    data1, data2 = data.split("\n\n")
    i = 0
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


def b(data):
    lines = data.split("\n\n")[0].split("\n")
    i = 0
    upper_bounds = {}
    lower_bounds = {}
    for line in lines:
        instructions = line.split("{")[-1]
        instructions = instructions[:-1].split(",")
        for inst in instructions[:-1]:
            condition = inst.split(":")[0]
            var_name, operator, val = re.split(r"([<>])", condition)
            if operator == "<":
                if var_name not in upper_bounds or upper_bounds[var_name] :


            
    return 0


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
#assert(b(data)==48020869073824)
#submit(b(data), part="b", year=year, day=day)
