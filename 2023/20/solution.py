from aocd import submit
from aocd.models import Puzzle

from collections import deque
import numpy as np


class FlipFlop:
    def __init__(self, name):
        self.name = name
        self.on = False
        self.connections = set()

    def add_connection(self, connection):
        self.connections.add(connection)

    def receive(self, signal, sender):
        if signal == 1:
            return []
        elif signal == 0:
            self.on = not self.on
            out_signals = ((c, int(self.on), self.name) for c in self.connections)
            return out_signals
        else:
            raise Exception
         
class Conjunction:
    def __init__(self, name):
        self.name = name
        self.on = False
        self.connections = set()
        self.inputs = {}

    def add_input(self, input):
        self.inputs[input] = 0

    def add_connection(self, connection):
        self.connections.add(connection)

    def receive(self, signal, sender):
        if signal != 1 and signal != 0:
            raise Exception
        self.inputs[sender] = signal
        self.on = all(self.inputs.values())
        return ((c, int(not self.on), self.name) for c in self.connections)
            
class Broadcast:
    def __init__(self, name):
        self.name = name
        self.connections = set()

    def add_connection(self, connection):
        self.connections.add(connection)

    def receive(self, signal, sender):
        if signal != 1 and signal != 0:
            raise Exception
        return ((c, signal, self.name) for c in self.connections)

class Tester:
    def __init__(self, name):
        self.name = name
        self.connections = set()

    def add_connection(self, connection):
        raise Exception("I am but a simple tester")

    def receive(self, signal, sender):
        return []

def get_nodes(data):
    nodes = {}
    connection_map = {}
    conjunctions = set()
    for line in data.split("\n"):
        source, connections = line.split("->")
        source = source.strip()
        if source == "broadcaster":
            name = source
            nodes[source] = Broadcast(name)
        elif source[0] == "%":
            name = source[1:]
            nodes[source[1:]] = FlipFlop(name)
        elif source[0] == "&":
            name = source[1:]
            conjunctions.add(name)
            nodes[source[1:]] = Conjunction(name)
        connection_map[name] = [x.strip() for x in connections.split(",")]
    for name, connections in connection_map.items():
        node = nodes[name]
        for con in connections:
                if con in nodes:
                    node.add_connection(con)
                    if con in conjunctions:
                        nodes[con].add_input(name)
                else:
                    nodes[con] = Tester(con)
                    node.add_connection(con)
    return nodes

def a(data):
    nodes = get_nodes(data)

    high_pulses = 0
    low_pulses = 0
    for _ in range(1000):
        signals = [("broadcaster", 0, "button")]
        while len(signals) > 0:
            new_signals = []
            for target, signal, sender in signals:
                if signal == 0:
                    low_pulses += 1
                else:
                    high_pulses += 1
                new_signals.extend(nodes[target].receive(signal, sender))
            signals = new_signals
    
    return high_pulses * low_pulses

def b(data):
    nodes = get_nodes(data)
    signal_queue = deque()
    rx_input_node = [n for n in nodes if "rx" in nodes[n].connections][0]
    rx_input_inputs = nodes[rx_input_node].inputs
    input_input_activations = {}
    i = 1
    while True:
        signal_queue.append(("broadcaster", 0, "button"))
        while signal_queue:
            target, signal, sender = signal_queue.popleft()
            if signal == 1 and sender in rx_input_inputs and sender not in input_input_activations:
                input_input_activations[sender] = i
                if len(input_input_activations) == len(rx_input_inputs):
                    return np.prod(np.lcm.reduce(list(input_input_activations.values())))
            for response in nodes[target].receive(signal, sender):
                signal_queue.append(response)
        i += 1



year = 2023
day = 20


p = Puzzle(year=year, day=day)
data = p.input_data


example_data_a = p.examples[0].input_data
example_answer_a = 32000000



example_data_a_2 = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""

example_answer_a_2 = 11687500

assert(a(example_data_a)==int(example_answer_a))
assert(a(example_data_a_2)==int(example_answer_a_2))
assert(a(data)==883726240)
#submit(a(data), part="a", year=year, day=day)


assert(b(data)==211712400442661)
#submit(b(data), part="b", year=year, day=day)