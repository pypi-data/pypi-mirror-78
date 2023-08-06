"""
Implements a standard logger class. This is a common interface to be used
throughout the library to make it easier to migrate between different logging
implementations with ease.
"""

import functools
import logging
import sys


def setup(debug: bool) -> None:
    """
    Sets the configuration for the logging parameter.
    """

    logging_level = logging.DEBUG if debug else logging.INFO

    formatter = logging.Formatter("[%(filename)12s:%(lineno)4d] \u001b[1m%(levelname)-8s\u001b[0m - %(message)s")

    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setLevel(logging_level)
    console_handler.setFormatter(formatter)

    log().setLevel(logging_level)
    log().addHandler(console_handler)


@functools.lru_cache(maxsize=None)
def log() -> logging.Logger:
    """
    Returns a Logger object.
    """

    return logging.getLogger("ochs")
