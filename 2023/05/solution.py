from aocd import submit
from aocd.models import Puzzle


def a(data):
    groups = data.split("\n\n")
    seeds = groups[0].split(":")[1].strip().split(" ")
    seeds = [int(x) for x in seeds]
    for group in groups[1:]:
        ranges = group.split("\n")[1:]
        ranges =[[int(x) for x in y.split()] for y in ranges]
        for i, seed in enumerate(seeds.copy()):
            for r in ranges:
                if seed >= r[1] and seed < r[1] + r[2]:
                    seeds[i] = r[0] + seed - r[1]
                    break
    return min(seeds)

def compare_all_ranges(ranges, seed_ranges, new_seed_ranges):
    for seed_start, seed_length in seed_ranges:
        for r in ranges:
            if seed_start >= r[1] and seed_start < r[1] + r[2]:
                if seed_start + seed_length <= r[1] + r[2]:
                    offset = seed_start - r[1]
                    new_seed_ranges.append((r[0] + offset, seed_length))
                    seed_length = 0
                    break
                else:
                    offset = seed_start - r[1]
                    new_length = r[1] + r[2] - seed_start
                    new_seed_ranges.append((r[0] + offset, new_length))
                    seed_start = r[1] + r[2]
                    seed_length -= new_length
            if seed_start + seed_length <= r[1] + r[2] and seed_start + seed_length  >= r[1]:
                new_seed_ranges.append((r[0], r[1] - seed_start))
                seed_length -= r[1] - seed_start
            if seed_start < r[1] and seed_start + seed_length > r[1] + r[2]:
                new_seed_ranges.append((r[0], r[2]))
                compare_all_ranges(ranges, [(r[1] + r[2], seed_length - r[2])], new_seed_ranges)
                seed_length = seed_start - r[1]
        if seed_length > 0:
            new_seed_ranges.append((seed_start, seed_length))

def b(data):
    groups = data.split("\n\n")
    seeds = groups[0].split(":")[1].strip().split(" ")
    seeds = [int(x) for x in seeds]
    seed_ranges = []
    for i in range(len(seeds)//2):
        seed_ranges.append((seeds[2*i], seeds[2*i+1]))
    for group in groups[1:]:
        ranges = group.strip().split("\n")[1:]
        ranges = [[int(x) for x in y.split()] for y in ranges]
        new_seed_ranges = []
        compare_all_ranges(ranges, seed_ranges, new_seed_ranges)
        seed_ranges = new_seed_ranges
    return min([x[0] for x in seed_ranges])



year = 2023
day = 5

p = Puzzle(year=year, day=day)
data = p.input_data

example_data_a = p.examples[0].input_data
example_answer_a = p.examples[0].answer_a

assert(a(example_data_a)==int(example_answer_a))
assert(a(data)==346433842)
# submit(a(data), part="a", year=year, day=day)


example_data_b = example_data_a
example_answer_b = 46

assert(b(example_data_b)==example_answer_b)
assert(b(data)==60294664)
# submit(b(data), part="b", year=year, day=day)
