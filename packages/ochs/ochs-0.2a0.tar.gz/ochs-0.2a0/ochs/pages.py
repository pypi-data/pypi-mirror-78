"""
Module handling pages.
"""

from functools import lru_cache
from typing import List, NamedTuple

import yaml

from ochs import logger, settings, templates, variables


class PageSpec(NamedTuple):
    """
    Specification for a page.
    """

    name: str
    template: str
    url: str
    is_blog_page: bool
    variables: List[variables.Variable]


class Page(NamedTuple):
    """
    A blog page.
    """

    url: str
    content: str


@lru_cache(maxsize=None)
def load_specs() -> List[PageSpec]:
    """
    Loads all the template specifications.
    """

    with open(settings.page_specs_path(), "r") as file:
        content = yaml.safe_load(file)

    return [
        PageSpec(
            name=raw_spec["name"],
            template=raw_spec["template"],
            url=raw_spec["url"],
            is_blog_page=raw_spec["is_blog_page"],
            variables=[
                variables.Variable(name=raw_variable["name"], value=raw_variable["value"])
                for raw_variable in raw_spec["load"]
            ],
        )
        for raw_spec in content
    ]


@lru_cache(maxsize=None)
def load(blog_pages: bool) -> List[Page]:
    """
    Loads all normal or blog pages.
    """

    logger.log().info(f"Loading relevant {'blog ' if blog_pages else ''}pages.")

    return [
        Page(
            url=page_spec.url,
            content=variables.expand(templates.load()[page_spec.template].content, page_spec.variables),
        )
        for page_spec in load_specs()
        if page_spec.is_blog_page == blog_pages
    ]
