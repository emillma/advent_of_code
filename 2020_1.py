from requests.api import get
from utils import get_data, submit


data = get_data(1, 2020)
data = [int(i) for i in data.splitlines()]
data = sorted(data)


def get_a(data, number=2020):
    i = 0
    j = len(data) - 1
    while (total := data[i] + data[j]) != number:
        if total > number:
            j -= 1
        else:
            i += 1

        if i == j:
            return None
    return data[i] * data[j]


def get_b(data, number=2020):
    for i in range(len(data)):
        rest = number - data[i]
        if (from_a := get_a(data[i+1:], rest)) is not None:
            return data[i] * from_a
