from utils import get_data, submit

data = get_data(3, 2020).splitlines()

width = len(data[0])

out = []
directions = [[1, 1],
              [3, 1],
              [5, 1],
              [7, 1],
              [1, 2]]
for step_y, step_x in directions: 
    y = 0
    x = 0
    count = 0
    while x < len(data):
        if data[x][y%width] == '#':
            count += 1
        y += step_y
        x += step_x
    out.append(count)
    print(count)