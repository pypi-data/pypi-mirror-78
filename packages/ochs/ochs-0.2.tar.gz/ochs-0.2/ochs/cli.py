"""
Implements the command line interface.
"""

import os
import shutil

import click

from ochs import logger, settings, website


@click.group()
@click.option("--debug/--no-debug", default=False)
def ochs(debug: bool) -> None:
    """
    Ochs: A tool for building static blogs.
    """

    logger.setup(debug)


@ochs.command()
def build() -> None:
    """
    Builds the blog.
    """

    logger.log().info("Building website.")
    website.build()


@ochs.command()
def pack() -> None:
    """
    Packs the blog into a zip folder.
    """

    logger.log().info("Packing website.")
    shutil.make_archive(os.path.expanduser("~/blog"), "zip", settings.target_folder())
