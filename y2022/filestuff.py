from pathlib import Path
from collections import UserDict
from dataclasses import dataclass, field
from typing import Generic, TypeVar
import re


@dataclass
class PathObject:
    name: str
    parent: "Dir"

    @property
    def path(self):
        path = f"{self.parent.path}/{self.name}" if self.parent else self.name
        return path[1:] if path.startswith("//") else path


@dataclass(repr=False)
class File(PathObject):
    size: int

    def __repr__(self):
        return f"File({self.path}, {self.size})"


@dataclass(repr=False)
class Dir(PathObject):
    children: dict[str, PathObject] = field(default_factory=dict, repr=False)

    def reldir(self, dirname: str, mkdir=False):
        current = self
        if dirname.startswith("/"):
            current = self.root()
        for part in dirname.split("/"):
            if part == "..":
                current = self.parent
            elif part == "." or part == "":
                pass
            elif mkdir:
                current = current.setdefault_dir(part)
        assert isinstance(current, Dir)
        return current

    def add_child(self, child: PathObject, existing_ok=False):
        if not existing_ok:
            assert child.name not in self.children
        return self.children.setdefault(child.name, child)

    def setdefault_dir(self, dirname: str):
        return self.add_child(Dir(dirname, self), existing_ok=True)

    def setdefault_file(self, filename: str, size: int):
        return self.add_child(File(filename, self, size), existing_ok=True)

    def root(self):
        if self.parent:
            return self.parent.root()
        else:
            return self

    def children_recurse(
        self, include_self=True, include_files=True, include_dirs=True
    ):
        def key(p: PathObject):
            return (isinstance(p, Dir), p.name)

        if include_self:
            yield self
        for child in sorted(self.children.values(), key=key):
            if isinstance(child, Dir) and include_dirs:
                yield from child.children_recurse(
                    include_self=include_dirs,
                    include_files=include_files,
                    include_dirs=include_dirs,
                )
            elif isinstance(child, File) and include_files:
                yield child

    def size(self):
        return sum(
            child.size if isinstance(child, File) else child.size()
            for child in self.children.values()
        )

    def print_tree(self, indent=0, print_dirs=True, print_files=True):
        print(" " * indent + repr(self))

        def key(p: PathObject):
            return (-isinstance(p, Dir), p.name)

        for child in sorted(self.children.values(), key=key):
            if isinstance(child, Dir) and print_dirs:
                child.print_tree(indent + 2)
            elif isinstance(child, File) and print_files:
                print(" " * (indent + 2) + repr(child))

    def __repr__(self):
        return f"Dir({self.path})"
