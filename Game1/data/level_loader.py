import csv


def load_level(level, rows, cols):
    world_data = []
    for row in range(rows):
        r = [-1] * cols
        world_data.append(r)
    # load level data
    with open(f'data/levels/level_map_{level}.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                world_data[x][y] = int(tile)

    return world_data
