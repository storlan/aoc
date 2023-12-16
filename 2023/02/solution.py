from aocd import submit
from aocd.models import Puzzle

import re

blue_re = r"([0-9]+) blue"
red_re = r"([0-9]+) red"
green_re = r"([0-9]+) green"

def extract_max(regex, text):
    return max([int(x) for x in re.findall(regex, text)])

def a(data):
    red_limit=12
    green_limit=13
    blue_limit=14
    ok_sum = 0
    for i, game in enumerate(data.split("\n")):
        green = extract_max(green_re, game)
        red = extract_max(red_re, game)
        blue = extract_max(blue_re, game)
        if blue <= blue_limit and green <= green_limit and red <= red_limit:
            ok_sum += i + 1
    return  ok_sum

def b(data):
    sum = 0
    for game in data.split("\n"):
        green = extract_max(green_re, game)
        red = extract_max(red_re, game)
        blue = extract_max(blue_re, game)
        sum += green * red * blue
    return sum

year = 2023
day = 2

p = Puzzle(year=year, day=day)
data = p.input_data

example_data_a = p.examples[0].input_data
example_answer_a = p.examples[0].answer_a

assert(a(example_data_a)==int(example_answer_a))
assert(a(data)==2551)
#submit(a(data), part="a", year=year, day=day)


example_data_b = example_data_a
example_answer_b = 2286

assert(b(example_data_b)==int(example_answer_b))
assert(b(data)==62811)
#submit(b(data), part="b", year=year, day=day)
