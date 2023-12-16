from aocd import submit
from aocd.models import Puzzle


direction_map = {
    "\\":{
        (-1, 0):[(0,-1)],
        (0,1):[(1,0)],
        (0,-1):[(-1,0)],
        (1,0):[(0,1)]
    },
    "/":{
        (-1, 0):[(0,1)],
        (0,1):[(-1,0)],
        (0,-1):[(1,0)],
        (1,0):[(0,-1)]
    },
    "-":{
        (-1, 0):[(0,1),(0,-1)],
        (0,1):[(0,1)],
        (0,-1):[(0,-1)],
        (1,0):[(0,-1), (0,1)]
    },
    "|":{
        (-1, 0):[(-1,0)],
        (0,1):[(1,0), (-1,0)],
        (0,-1):[(1,0), (-1,0)],
        (1,0):[(1,0)]
    },
    ".":{
        (-1, 0):[(-1, 0)],
        (0,1):[(0,1)],
        (0,-1):[(0,-1)],
        (1,0):[(1,0)]
    }
}

def energized_tiles(start_dir, start_tile, tiles):
    height = len(tiles)
    width = len(tiles[0])
    energized = set()
    beams = [(start_dir[0], start_dir[1], start_tile[0], start_tile[1])]
    new_beams = []
    traveled = set()
    while len(beams) > 0:
        new_beams = []
        for i, beam in enumerate(beams):
            dir_r, dir_c, coord_r, coord_c = beam
            energized.add((coord_r, coord_c))
            traveled.add(beam)
            tile = tiles[coord_r][coord_c]
            for direction in direction_map[tile][(dir_r, dir_c)]:
                new_coord = (coord_r + direction[0], coord_c + direction[1])
                if new_coord[0] < 0 or new_coord[0] >= height or new_coord[1] < 0 or new_coord[1] >= width:
                    continue
                new_beam = (direction[0], direction[1], new_coord[0], new_coord[1])
                if new_beam not in traveled:
                    new_beams.append(new_beam)
        beams = new_beams
    return energized

def a(data):
    data_rows = []
    for line in data.split("\n"):
        data_rows.append(list(line))
    energized = energized_tiles((0, 1), (0, 0), data_rows)
    return len(energized)

def b(data):
    tiles = []
    for line in data.split("\n"):
        tiles.append(list(line))
    height = len(tiles)
    width = len(tiles[0])
    best = 0
    for row in range(height):
        best = max(len(energized_tiles((0, 1), (row, 0), tiles)), best)
        best = max(len(energized_tiles((0, -1), (row, width - 1), tiles)), best)
    for col in range(width):
        best = max(len(energized_tiles((1, 0), (0, col), tiles)), best)
        best = max(len(energized_tiles((-1, 0), (height - 1, col), tiles)), best)
    return best

year = 2023
day = 16

p = Puzzle(year=year, day=day)
data = p.input_data

example_data_a = p.examples[0].input_data
example_answer_a = p.examples[0].answer_a

assert(a(example_data_a)==int(example_answer_a))
assert(a(data)==7939)
#submit(a(data), part="a", year=year, day=day)

example_data_b = example_data_a
example_answer_b = 51

assert(b(example_data_b)==example_answer_b)
assert(b(data)==8318)
#submit(b(data), part="b", year=year, day=day)
