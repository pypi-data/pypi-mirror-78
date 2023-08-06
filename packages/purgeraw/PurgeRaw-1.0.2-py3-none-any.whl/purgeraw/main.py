from typing import Tuple

import click
from toolz import pipe  # type: ignore

from purgeraw import __version__
from purgeraw.directory_walker import directory_walker
from purgeraw.deletion import fake_deleter, deleter
from purgeraw.index_extraction import indexer
from purgeraw.purger import purge


@click.command("praw")
@click.option("-i", "--input", "input_path", required=True, type=click.Path(exists=True), metavar="<directory>",
              help="Directory of processed and raw images to be purged.")
@click.option("-d", "--delete", "do_delete", is_flag=True,
              help="By default praw will just explain what would be removed. A"
                   "dd this flag to perform the deletion.")
@click.option("-r", "--raw_exts", multiple=True, type=str, default=["cr3", "xmp"], show_default=True, metavar="<ext>",
              help="Used to override the default extensions of raw files. "
                   "Can be specified multiple times for each raw type e.g. -r cr3 -r cr2 -r raw.")
@click.option("-p", "--processed_exts", multiple=True, type=str, default=["jpg"], show_default=True, metavar="<ext>",
              help="Used to override the default extensions of processed images. "
                   "Can also be specified multiple times as -r above.")
@click.version_option(__version__, prog_name="praw")
def main(input_path: str, do_delete: bool, raw_exts: Tuple[str], processed_exts: Tuple[str]) -> None:
    """Trawls the input directory for raw and processed images.
    Where it finds a raw image with a numeric index that can't be
    found in the processed images it is marked for removal.

    Any sequence of 3 to 6 (inc) numbers in the image filename is deemed as its index which is used
    to associate processed and raw images.

    Processed images may also have a filename format with a range of indexes, e.g. IMG_01234-1236.jpg
    This processed file would be associated with IMG_01234.cr3, IMG_01235.cr3 and IMG_01236.cr3 raw images
    thus ensuring they are not deleted. This is useful for HDR or panoramic processed images.
    """
    pipe(
        input_path,
        directory_walker(list(raw_exts + processed_exts)),
        purge(list(raw_exts), indexer),
        deleter if do_delete else fake_deleter
    )


if __name__ == "__main__":
    main()
