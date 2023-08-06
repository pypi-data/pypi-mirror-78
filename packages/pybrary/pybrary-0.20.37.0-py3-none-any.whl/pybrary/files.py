from re import compile
from os import scandir
from operator import attrgetter
from pathlib import Path


def files(path):
    with scandir(path) as ls:
        for fil in sorted(ls, key=attrgetter('path')):
            if fil.is_dir(follow_symlinks=False):
                yield from files(fil.path)
            elif fil.is_file():
                yield fil.path


def find(path, name):
    match = compile(name).search
    for fil in files(path):
        if match(fil):
            yield Path(fil)


