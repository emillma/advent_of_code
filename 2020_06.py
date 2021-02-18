from utils import get_data, submit
import numpy as np

data = get_data(6, 2020).splitlines()


def group_gen(data):
    out = []
    for line in data:
        if line:
            out.append(line)
        else:
            yield out
            out = []
    yield out


def count_any(group):
    return len(set(''.join(group)))


def count_all(group):
    table = np.zeros((len(group), 26), int)
    for i, person in enumerate(group):
        for question in person:
            table[i, ord(question) - ord('a')] = 1
    return sum(table.all(axis=0))


ans1 = sum([count_any(i) for i in group_gen(data)])
ans2 = sum([count_all(i) for i in group_gen(data)])
