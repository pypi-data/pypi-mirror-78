import os
from typing import List
from toolz import curry   # type: ignore


@curry
def directory_walker(exts: List[str], directory: str) -> List[str]:
    chosen = []

    for root, _, files in os.walk(directory):
        chosen += [os.path.join(root, file) for file in files if any(map(file.lower().endswith, exts))]

    return chosen
