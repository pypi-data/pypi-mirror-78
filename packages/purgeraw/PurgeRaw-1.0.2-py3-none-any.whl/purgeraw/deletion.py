import os
from typing import List


def fake_deleter(paths: List[str]) -> None:
    for path in paths:
        print(f"DRYRUN: Deleted {path}")


def deleter(paths: List[str]) -> None:
    for path in paths:
        os.remove(path)
        print(f"Deleted {path}")
