from utils import get_data, submit
import numpy as np
import re


# basically an asyclic graph
data = get_data(7, 2020).splitlines()


def parse(text):
    match = re.match(r'(.*) bags contain (.*)', text)
    top_bag = match.group(1)
    match = re.finditer(r'(\d+) (.*?) bags?', match.group(2))
    inside = dict([(i.group(2), int(i.group(1))) for i in match])
    return [top_bag, inside]


rules = [parse(i) for i in data]


def get_bags_that_might_contain_gold(rules):
    special = 'shiny gold'
    valid = set()
    totest = set([r[0] for r in rules if special in r[1].keys()])
    while totest:
        current = totest.pop()
        valid.add(current)
        candidates = [r for r in rules if current in r[1].keys()]
        totest.update((c[0] for c in candidates if c[0] not in valid))
    return len(valid)


ans1 = get_bags_that_might_contain_gold(rules)

rules_dict = dict(rules)


def get_child_count(current_bag):
    total = 1
    for bag, count in rules_dict[current_bag].items():
        total += get_child_count(bag) * count
    return total


ans2 = get_child_count('shiny gold')-1
