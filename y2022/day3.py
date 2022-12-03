from utils import AocClient
import re


class Bag:
    def __init__(self, line):
        self.comp1 = line[: len(line) // 2]
        self.comp2 = line[len(line) // 2 :]

        assert len(self.comp1) == len(self.comp2) and len(self.comp1) + len(
            self.comp2
        ) == len(line)

    @staticmethod
    def chr_to_num(chr):
        if ord("a") <= ord(chr) <= ord("z"):
            return ord(chr) - ord("a") + 1
        elif ord("A") <= ord(chr) <= ord("Z"):
            return ord(chr) - ord("A") + 27

    def in_both_comps(self):
        intersection = set(self.comp1).intersection(set(self.comp2))
        assert len(intersection) == 1
        return intersection.pop()

    def __iter__(self):
        for item in self.comp1 + self.comp2:
            yield item


client = AocClient.from_this_file()
data = client.get_input(use_example_data=False)
bags = [Bag(line) for line in data.split("\n") if line]
ans = sum([Bag.chr_to_num(bag.in_both_comps()) for bag in bags])
client.submit(level=1, answer=ans)
"""Part 2"""


class Group:
    def __init__(self, bag1, bag2, bag3):
        self.bag1 = bag1
        self.bag2 = bag2
        self.bag3 = bag3

    def intersection_all(self):
        inter = set(self.bag1).intersection(set(self.bag2)).intersection(set(self.bag3))
        assert len(inter) == 1
        return inter.pop()


groups = [Group(*bags[i : i + 3]) for i in range(0, len(bags), 3)]
ans = sum([Bag.chr_to_num(group.intersection_all()) for group in groups])
client.submit(level=2, answer=ans)
