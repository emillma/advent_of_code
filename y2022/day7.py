import re
from utils import AocClient
import itertools
from pathlib import Path
from dataclasses import KW_ONLY, InitVar, dataclass, field
from typing import ClassVar
from collections import UserDict
from filestuff import File, Dir


@dataclass
class Command:
    name: str
    args: str
    output_lines: list[str]

    @classmethod
    def from_tape(cls, input_lines: list[str]):
        command_line = input_lines.pop(0)
        match = re.match(r"\$ (\w+) ?(.*)", command_line)
        assert match
        name = match.group(1)
        args = match.group(2)

        output_lines = []
        while input_lines and input_lines[0][0] != "$":
            output_lines.append(input_lines.pop(0))
        return cls(name, args, output_lines)

    @classmethod
    def parse_multiple_commands(cls, input_lines: list[str]):
        input_lines = input_lines.copy()
        commands = []
        while input_lines:
            commands.append(cls.from_tape(input_lines))
        return commands

    def __repr__(self):
        output = ",".join(self.output_lines) if self.output_lines else "None"
        return f"$ {self.name} {self.args} -> {output}"


class Terminal:
    def __init__(self, file_system: Dir):
        self.current_dir = file_system

    def cd(self, dirname: str, output_lines, mkdir=True):
        self.current_dir = self.current_dir.reldir(dirname, mkdir=mkdir)

    def ls(self, dirname: str, output_lines, touch=True):
        dir = self.current_dir.reldir(dirname)
        for line in output_lines:
            if m := re.match(r"(\d+) ([\w\.]+)", line):
                dir.setdefault_file(m.group(2), int(m.group(1)))
            elif m := re.match(r"dir ([\w\.]+)", line):
                dir.setdefault_dir(m.group(1))
            else:
                raise NotImplementedError(f"ls output line {line} not implemented")

    def execute(self, command: Command):
        if hasattr(self, command.name):
            # print(command)
            output = getattr(self, command.name)(command.args, command.output_lines)
            # print(f"{self.current_dir.path}: {command.name} -> {command.output_lines}")
            return output
        else:
            raise NotImplementedError(f"Command {command.name} not implemented")


client = AocClient.from_this_file()
data = client.get_input(use_example_data=False)

commands = Command.parse_multiple_commands(data.splitlines())
file_system = Dir("/", None)
terminal = Terminal(file_system)
for command in commands:
    terminal.execute(command)

alldirs = list(file_system.children_recurse(include_files=False))
dirsizes = [dir.size() for dir in alldirs]
ans = sum(size for size in dirsizes if size <= 100000)
print(ans)
client.submit(level=1, answer=ans)


"""part 2"""
ans2 = min(
    size for size in dirsizes if 70000000 - file_system.size() + size >= 30000000
)
client.submit(level=2, answer=ans2)
