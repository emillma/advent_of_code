from utils import AocClient
import re
import numpy as np
from copy import deepcopy


class Move:
    def __init__(self, move_str):
        match = re.match(r"move (\d+) from (\d+) to (\d+)", move_str).groups()
        self.number, self.origin, self.target = map(int, match)
        self.origin -= 1
        self.target -= 1

    def __repr__(self):
        return f"Move({self.number}, {self.origin}, {self.target})"

    def apply(self, table):
        ...


class Table:
    def __init__(self, table_str):
        lines = table_str.split("\n")
        column_numbers = list(map(int, re.findall(r"\d+", lines[-1])))

        crate_lines = lines[0:-1]
        stacks = [[] for i in range(len(column_numbers))]
        for row in range(len(crate_lines) - 1, -1, -1):
            line = crate_lines[row]
            col = 0
            while part := line[:4]:
                line = line[4:]
                if set(part) != {" "}:
                    stacks[col].append(part[1])
                col += 1
        self.stacks = stacks

    def rearange(self, moves: list[Move]):
        stacks = deepcopy(self.stacks)
        for move in moves:
            for n in range(move.number):
                stacks[move.target].append(stacks[move.origin].pop())
        return stacks

    def rearange1(self, moves: list[Move]):
        stacks = deepcopy(self.stacks)
        for move in moves:
            stacks[move.target].extend(stacks[move.origin][-move.number :])
            stacks[move.origin] = stacks[move.origin][: -move.number]
        return stacks


client = AocClient.from_this_file()
data = client.get_input(use_example_data=False)

table_str, moves_str = data.split("\n\n")


table = Table(table_str)
moves = [Move(move_str) for move_str in moves_str.split("\n") if move_str]
ans = "".join(stack[-1] for stack in table.rearange(moves))

client.submit(level=1, answer=ans)

ans2 = "".join(stack[-1] for stack in table.rearange1(moves))
client.submit(level=2, answer=ans2)
