"""
Holds library level settings for PyBlog.
"""

import os
from functools import lru_cache

SETTINGS_FOLDER = "settings"


@lru_cache(maxsize=None)
def source_folder() -> str:
    """
    Returns the absolute path of the source folder.
    """

    return os.path.expandvars(os.getenv("OCHS_SOURCE", "$HOME/blog"))


@lru_cache(maxsize=None)
def target_folder() -> str:
    """
    Returns the absolute path of the target folder.
    """

    return os.path.expandvars(os.getenv("OCHS_TARGET", "$HOME/blog-build"))


@lru_cache(maxsize=None)
def templates_folder() -> str:
    """
    Returns the absolute path of the template folder.
    """

    return os.path.join(source_folder(), "templates")


@lru_cache(maxsize=None)
def resources_folder() -> str:
    """
    Returns the absolute path of the resources folder.
    """

    return os.path.join(source_folder(), "resources")


@lru_cache(maxsize=None)
def posts_folder() -> str:
    """
    Returns the absolute path of the posts folder.
    """

    return os.path.join(source_folder(), "posts")


@lru_cache(maxsize=None)
def variables_path() -> str:
    """
    Returns the absolute path of the variables file.
    """

    return os.path.join(source_folder(), SETTINGS_FOLDER, "variables.yaml")


@lru_cache(maxsize=None)
def template_specs_path() -> str:
    """
    Returns the absolute path of the templates file.
    """

    return os.path.join(source_folder(), SETTINGS_FOLDER, "templates.yaml")


@lru_cache(maxsize=None)
def page_specs_path() -> str:
    """
    Returns the absolute path of the pages file.
    """

    return os.path.join(source_folder(), SETTINGS_FOLDER, "pages.yaml")


@lru_cache(maxsize=None)
def post_specs_path() -> str:
    """
    Returns the absolute path of the posts file.
    """

    return os.path.join(source_folder(), SETTINGS_FOLDER, "posts.yaml")
