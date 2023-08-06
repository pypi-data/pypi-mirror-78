import argparse
import logging
import os
from typing import Optional
from typing import Sequence

from keats import Keats
from keats.hooks.utils import added_files

logger = logging.getLogger("keats_version_up")
logger.setLevel("DEBUG")


def version_up():
    logger.debug("initializing Keats() at {}".format(os.getcwd()))
    keats = Keats()
    logger.info("__version__.py at {}".format(keats.version._get_version_path()))
    keats.version.up()


PYPROJECT = "pyproject.toml"


def run(filenames):
    retv = 0
    trigger_files = {PYPROJECT}
    _added_files = added_files()
    files = _added_files & set(filenames)
    triggered_files = trigger_files.intersection(files)

    logger.debug("Added files: {}".format(_added_files))
    logger.debug("Pre-commit files: {}".format(set(filenames)))
    logger.debug("Trigger files: {}".format(trigger_files))
    logger.debug("Triggered files: {}".format(triggered_files))

    if triggered_files:
        keats = Keats()
        keats.version.up()
        retv = 1
    else:
        logger.debug("No changes to be made.")
    # else:
    #     keats = Keats()
    #     if not keats.version._exists():
    #         keats.version.up()
    return retv


def parse_args(argv):
    if argv is None:
        argv = []
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filenames",
        nargs="*",
        help="Filenames pre-commit believes are changed.",
        default=[],
    )
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Verbosity (-v, -vv, -vvv)"
    )
    args = parser.parse_args(argv)
    return args


def main(argv: Optional[Sequence[str]] = None) -> int:
    logger.error("main: argv: {}".format(argv))
    args = parse_args(argv)
    if args.verbose == 3:
        logger.setLevel("DEBUG")
    elif args.verbose == 2:
        logger.setLevel("INFO")
    elif args.verbose == 1:
        logger.setLevel("WARNING")
    logger.debug("Args: {}".format(args))
    return run(args.filenames)


if __name__ == "__main__":
    exit(main())
