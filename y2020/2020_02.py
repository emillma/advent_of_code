from utils import get_data, submit
import re

data = get_data(2, 2020).splitlines()


def get_a(data):
    pattern = r'(\d+)-(\d+) ([a-z]): ([a-z]*)'
    count = 0
    for line in data:
        low, high, cha, pas = re.match(pattern, line).groups()
        if int(low) <= pas.count(cha) <= int(high):
            count += 1
    return count


def get_b(data):
    pattern = r'(\d+)-(\d+) ([a-z]): ([a-z]*)'
    count = 0
    for line in data:
        first, last, cha, pas = re.match(pattern, line).groups()
        if (pas[int(first)-1] == cha) ^ (pas[int(last)-1] == cha):
            count += 1
    return count


ans = get_a(data)
ans2 = get_b(data)
