from utils import get_data, submit
import numpy as np

data = get_data(5, 2020).splitlines()


def seat_to_pos(seat):
    i = seat[:7]
    j = seat[7:]

    i = i.replace('F', '0').replace('B', '1')
    j = j.replace('L', '0').replace('R', '1')
    i = int(i, 2)
    j = int(j, 2)
    return i, j


def pos_to_id(i, j):
    return i*8 + j


def seat_to_id(seat):
    return pos_to_id(*seat_to_pos(seat))


print(max([seat_to_id(seat) for seat in data]))

plane = np.ones((2**7, 2**3))
for line in data:
    seat = seat_to_pos(line)
    plane[seat] = 0

free = [i for i in np.argwhere(plane)]
ids = [seat_to_id(i) for i in data]
free = [i for i in free if pos_to_id(*i)+1 in ids and pos_to_id(*i)-1 in ids]
print(pos_to_id(*free[0]))
