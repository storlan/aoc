import numpy as np
from aocd import submit
from aocd.models import Puzzle


def a(data):
    sum = 0

    for line in data.split("\n"):
        winners, numbers = line.split("|")
        winners = winners.split(":")[-1].split(" ")
        winners = set([int(x) for x in winners if len(x) > 0])
        numbers = numbers.split(" ")
        numbers = set([int(x) for x in numbers if len(x) > 0])
        hits = len(winners.intersection(numbers))
        if hits > 0:
            sum += 2 ** (hits - 1)
    return sum

def b(data):
    lines = data.split("\n")
    scratch_cards = np.ones(len(lines), dtype=int)

    for i, line in enumerate(lines):
        winners, numbers = line.split("|")
        winners = winners.split(":")[-1].split(" ")
        winners = set([int(x) for x in winners if len(x) > 0])
        numbers = numbers.split(" ")
        numbers = set([int(x) for x in numbers if len(x) > 0])
        hits = len(winners.intersection(numbers))
        multiplier = scratch_cards[i]
        scratch_cards[i+1:min(hits+1+i, len(scratch_cards))] += multiplier
    return scratch_cards.sum()


year = 2023
day = 4

p = Puzzle(year=year, day=day)
data = p.input_data

example_data_a = p.examples[0].input_data
example_answer_a = p.examples[0].answer_a

assert(a(example_data_a)==int(example_answer_a))
assert(a(data)==27059)
#submit(a(data), part="a", year=year, day=day)


example_data_b = example_data_a
example_answer_b = 30

assert(b(example_data_b)==example_answer_b)
assert(b(data)==5744979)
#submit(b(data), part="b", year=year, day=day)
