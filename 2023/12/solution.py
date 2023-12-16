from aocd import submit
from aocd.models import Puzzle

from functools import lru_cache

@lru_cache
def traverse_string(string, groups, string_pos=0, spring_count=0, current_group=0):
    if string_pos == len(string):
        if spring_count > 0:
            if current_group < len(groups) and spring_count == groups[current_group]:
                current_group += 1
            else:
                return 0
        return current_group == len(groups)
    current_char = string[string_pos]
    if current_char == "?":
        count = 0
        if current_group < len(groups) and spring_count + 1 <= groups[current_group]:
            count += traverse_string(string, groups, string_pos + 1, spring_count + 1, current_group)
        if spring_count > 0:
            if current_group < len(groups) and spring_count == groups[current_group]:
                count += traverse_string(string, groups, string_pos + 1, 0, current_group+1)
        else:
            count += traverse_string(string, groups, string_pos + 1, spring_count, current_group)
        return count
    elif current_char == "#":
        spring_count += 1
        return traverse_string(string, groups, string_pos + 1, spring_count, current_group)
    elif current_char == ".":
        if spring_count > 0:
            if current_group < len(groups) and spring_count == groups[current_group]:
                current_group += 1
                spring_count = 0
            else:
                return 0
        return traverse_string(string, groups, string_pos + 1, spring_count, current_group)
    else:
        raise Exception("Wat")


def a(data):
    total = 0
    for line in data.split("\n"):
        springs, groups = line.split(" ")
        groups = tuple([int(x) for x in groups.split(",")])
        count = traverse_string(springs, groups)
        total += count
    return total

def b(data):
    total = 0
    for line in data.split("\n"):
        springs, groups = line.split(" ")
        groups = tuple([int(x) for x in groups.split(",")] * 5)
        springs = "?".join([springs]*5)
        count = traverse_string(springs, groups)
        total += count
    return total

year = 2023
day = 12

p = Puzzle(year=year, day=day)
data = p.input_data

example_data_a = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""
example_answer_a = p.examples[0].answer_a

assert(a(example_data_a)==int(example_answer_a))
assert(a(data)==7732)
#submit(a(data), part="a", year=year, day=day)

example_data_b = example_data_a
example_answer_b = 525152

assert(b(example_data_b)==example_answer_b)
assert(b(data)==4500070301581)
#submit(b(data), part="b", year=year, day=day)
