from re import compile
from os import scandir
from operator import attrgetter
from pathlib import Path


def files(path):
    with scandir(path) as ls:
        for entry in sorted(ls, key=attrgetter('path')):
            if entry.is_dir(follow_symlinks=False):
                yield from files(entry.path)
            elif entry.is_file():
                yield entry.path


def find(path, name):
    match = compile(name).search
    for full in files(path):
        if match(full):
            yield Path(full)


