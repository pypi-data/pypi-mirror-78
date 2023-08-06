"""
Implements actual website-building functionality.
"""

import os
import shutil

from ochs import blog, logger, pages, settings


def _clean_target_folder() -> None:
    """
    If the target folder already exists, remove it.
    """

    if os.path.exists(settings.target_folder()):
        if not os.path.isdir(settings.target_folder()):
            raise NotADirectoryError(f"'{settings.target_folder()}' is not a directory.")

        shutil.rmtree(settings.target_folder())


def _build_pages() -> None:
    """
    Builds the static load in the target folder.
    """

    for page in pages.load(blog_pages=False):
        logger.log().info(f"Writing page '{page.url}'.")

        page_filepath = os.path.join(settings.target_folder(), page.url)
        with open(page_filepath, "w") as file:
            file.write(page.content)


def _build_blog_pages() -> None:
    """
    Builds the static blog load in the target folder.
    """

    for page in blog.blog_pages():
        logger.log().info(f"Writing blog page '{page.url}'.")

        page_filepath = os.path.join(settings.target_folder(), page.url)
        with open(page_filepath, "w") as file:
            file.write(page.content)


def _build_blog_posts() -> None:
    """
    Builds the load for the blog posts in the target folder.
    """

    for page in blog.post_pages():
        logger.log().info(f"Writing post '{page.url}'.")

        page_filepath = os.path.join(settings.target_folder(), page.url)
        with open(page_filepath, "w") as file:
            file.write(page.content)


def _copy_resources() -> None:
    """
    Copies the resources into the target folder.
    """

    logger.log().info("Copying resources.")
    shutil.copytree(settings.resources_folder(), settings.target_folder())


def build() -> None:
    """
    Builds the website.
    """

    _clean_target_folder()
    _copy_resources()
    _build_pages()
    _build_blog_pages()
    _build_blog_posts()
