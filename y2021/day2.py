from utils import AocClient
import numpy as np
import re

client = AocClient.from_this_file()


class Mov:
    def __init__(self, line):
        self.direction = line.split(" ")[0]
        self.magnitude = int(line.split(" ")[1])

    @property
    def array(self):
        if self.direction == "forward":
            return np.array([self.magnitude, 0])
        elif self.direction == "down":
            return np.array([0, self.magnitude])
        elif self.direction == "up":
            return np.array([0, -self.magnitude])

    def __repr__(self):
        return f"{self.direction} {self.magnitude}"


data = client.get_input(use_example_data=False)

movements = [Mov(line) for line in data.splitlines()]
pos = sum(mov.array for mov in movements)
ans = pos[0] * pos[1]

"""Task2"""
data = client.get_input(use_example_data=False)


class Mov2(Mov):
    def array(self, prev):
        if self.direction == "forward":
            return np.array([self.magnitude, prev[2] * self.magnitude, 0])
        elif self.direction == "down":
            return np.array([0, 0, self.magnitude])
        elif self.direction == "up":
            return np.array([0, 0, -self.magnitude])


state = np.zeros(3)
for line in data.splitlines():
    state += Mov2(line).array(state)
    print(state)

client.submit(2, state[0] * state[1])
# print(state)
# client.submit(1, ans)
