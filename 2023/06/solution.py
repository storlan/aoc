from aocd import submit
from aocd.models import Puzzle


def a(data):
    times, distances = data.split("\n")
    times = times.split(":")[-1].split()
    times = [int(t) for t in times]
    distances = distances.split(":")[-1].split()
    distances = [int(t) for t in distances]
    win_ways = 1
    for race_time, distance_to_beat in zip(times, distances):
        wins = 0
        for hold_time in range(race_time):
            distance_traveled = hold_time * (race_time - hold_time)
            if distance_traveled > distance_to_beat:
                wins += 1
        win_ways *= wins

    return win_ways

def b(data):
    time, distance = data.split("\n")
    time = time.split(":")[-1].split()
    time = int("".join(time))
    distance = distance.split(":")[-1].split()
    distance = int("".join(distance))
    wins = 0
    for hold_time in range(time):
        distance_traveled = hold_time * (time - hold_time)
        if distance_traveled > distance:
            wins += 1
    return wins

year = 2023
day = 6

p = Puzzle(year=year, day=day)
data = p.input_data

example_data_a = p.examples[0].input_data
example_answer_a = 288

assert(a(example_data_a)==int(example_answer_a))
assert(a(data)==293046)
#submit(a(data), part="a", year=year, day=day)


example_data_b = example_data_a
example_answer_b = 71503

assert(b(example_data_b)==example_answer_b)
assert(b(data)==35150181)
#submit(b(data), part="b", year=year, day=day)
