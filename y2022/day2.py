from utils import AocClient
import re

client = AocClient.from_this_file()


class Round:
    def __init__(self, round):
        self.abc, self.xyz = round.split(" ")
        self.them = self.abc_to_num(self.abc)
        self.me = self.xyz_to_num(self.xyz)
        self.rps_score = self.rock_paper_scissors(self.me, self.them)

    @property
    def score(self):
        return (self.rps_score + 1) * 3 + self.me + 1

    @staticmethod
    def abc_to_num(abd):
        return ord(abd) - 65

    @staticmethod
    def xyz_to_num(xyz):
        return ord(xyz) - 88

    @staticmethod
    def rock_paper_scissors(a, b):
        if a == b:
            return 0
        elif (a - b) % 3 == 1:
            return 1
        else:
            return -1


"""Part 1"""
data = client.get_input(use_example_data=False)
rounds = [Round(line) for line in data.split("\n") if line]

ans = sum([r.score for r in rounds])
client.submit(level=1, answer=ans)


"""Part 2"""


class Round2(Round):
    def __init__(self, round):
        self.abc, self.xyz = round.split(" ")

        self.them = self.abc_to_num(self.abc)
        self.me = (self.xyz_to_num(self.xyz) - 1 + self.them) % 3
        self.rps_score = self.rock_paper_scissors(self.me, self.them)


data = client.get_input(use_example_data=False)
rounds = [Round2(line) for line in data.split("\n") if line]

ans = sum([r.score for r in rounds])
client.submit(level=2, answer=ans)
# data = client.get_input(use_example_data=False)
