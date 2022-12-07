from utils import AocClient
import re

client = AocClient.from_this_file()
data = client.get_input(use_example_data=False)


class Pair:
    def __init__(self, line):
        a1, a2, b1, b2 = map(int, re.match(r"(\d+)-(\d+),(\d+)-(\d+)", line).groups())

        self.sec1 = set(range(a1, a2 + 1))
        self.sec2 = set(range(b1, b2 + 1))

    def __repr__(self):
        return f"Pair({self.sec1}, {self.sec2})"

    def one_is_subset(self):
        return self.sec1.issubset(self.sec2) or self.sec2.issubset(self.sec1)

    def overlap(self):
        return bool(self.sec1.intersection(self.sec2))


pairs = [Pair(line) for line in data.split("\n") if line]
ans = sum([pair.one_is_subset() for pair in pairs])
client.submit(level=1, answer=ans)

ans2 = sum([pair.overlap() for pair in pairs])
client.submit(level=2, answer=ans2)
