import os
import re
from re import Match
from typing import Tuple, List, Optional

SINGLE_IMAGE_INDEX_RE = re.compile("^.*?([0-9]{3,6}).*$")
RANGE_IMAGE_INDEX_RE = re.compile("^.*?([0-9]{3,6})-([0-9]{3,6}).*$")


def indexer(path: str) -> List[Tuple[str, str]]:

    range_matcher: Optional[Match[str]] = RANGE_IMAGE_INDEX_RE.match(os.path.basename(path))

    if range_matcher:
        size_1: int = len(range_matcher.group(1))
        size_2: int = len(range_matcher.group(2))
        start: int = int(range_matcher.group(1))
        end: int = int(range_matcher.group(2))

        if (end - start > 200) or (end - start < 0) or (size_1 != size_2):
            return []

        return [(("{:0" + str(size_1) + "d}").format(x), path) for x in range(start, end + 1)]

    single_matcher: Optional[Match[str]] = SINGLE_IMAGE_INDEX_RE.match(os.path.basename(path))

    if single_matcher:
        return [(single_matcher.group(1), path)]

    return []
