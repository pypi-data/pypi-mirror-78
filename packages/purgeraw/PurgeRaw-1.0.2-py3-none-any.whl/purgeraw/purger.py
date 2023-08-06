import os
from itertools import chain
from typing import List, Callable, Dict, Tuple
from toolz import curry   # type: ignore


def __is_raw(path: str, raw_exts: List[str]) -> bool:
    path_ext = os.path.splitext(path)[1].strip(".")
    return any((path_ext.lower() == ext.lower() for ext in raw_exts))


@curry
def purge(raw_exts: List[str],
          indexes: Callable[[str], List[Tuple[str, str]]],
          files
          ) -> List[str]:
    print(f"There are {len(files)} files to process")

    raw_files: Dict[str, str] = dict([indexes(file)[0] for file in files if __is_raw(file, raw_exts)])
    print(f"Found {len(raw_files)} raw files")

    processed_files: Dict[str, str] = dict(
        chain.from_iterable([indexes(file) for file in files if not __is_raw(file, raw_exts)]))
    print(f"Found {len(processed_files)} processed files")

    to_remove: List[str] = [raw_files[raw_index] for raw_index in raw_files.keys() if
                            raw_index not in processed_files.keys()]
    to_remove.sort()

    print(f"Found {len(to_remove)} files to remove: {to_remove}")

    return to_remove
