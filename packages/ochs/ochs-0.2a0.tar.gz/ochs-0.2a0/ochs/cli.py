"""
Implements the command line interface.
"""

import click

from ochs import logger, website


@click.group()
@click.option("--debug/--no-debug", default=False)
def blog(debug: bool) -> None:
    """
    PyBlog  - tool for building static blogs.
    """

    logger.setup(debug)


@blog.command()
def build() -> None:
    """
    Builds the blog.
    """

    logger.log().info("Building website.")
    website.build()
