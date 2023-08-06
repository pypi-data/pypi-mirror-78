"""
Module handling posts and blog specific pages.
"""

import os
import re
from datetime import date
from functools import lru_cache
from typing import List, NamedTuple, Tuple

import yaml
from markdown import markdown  # type: ignore

from ochs import logger, pages, settings, templates


class PostSpec(NamedTuple):
    """
    Specification for a post.
    """

    title: str
    date: date
    author: str
    preview: str
    content: str
    url: str
    template: templates.Template

    def transform(self, content: str) -> str:
        """
        Expands post variables.
        """

        return (
            content.replace("#{post-title}", self.title)
            .replace("#{post-date}", self.date.strftime("%Y/%m/%d"))
            .replace("#{post-author}", self.author)
            .replace("#{post-preview}", self.preview)
            .replace("#{post-content}", self.content)
            .replace("#{post-url}", self.url)
        )


def load_post_file(filename: str) -> str:
    """
    Loads a post file.
    """

    with open(os.path.join(settings.posts_folder(), filename), "r") as file:
        content = file.read()

    return markdown(content)


@lru_cache(maxsize=None)
def post_specs() -> List[PostSpec]:
    """
    Return post configuration.
    """

    with open(settings.post_specs_path(), "r") as file:
        content = yaml.safe_load(file)

    return sorted(
        [
            PostSpec(
                title=raw_spec["title"],
                date=date.fromisoformat(raw_spec["date"]),
                author=raw_spec["author"],
                preview=load_post_file(raw_spec["preview"]),
                content=load_post_file(raw_spec["content"]),
                url=raw_spec["url"],
                template=templates.load()[raw_spec["template"]],
            )
            for raw_spec in content
        ],
        key=lambda spec: spec.date,
        reverse=True,
    )


def _clean_block(raw_block: str) -> Tuple[str, int]:
    """
    Remove the #{post-start} and #{post-end} flags, and the post count, returning
    a clean block and the post count separately.
    """

    raw_block = raw_block[len("#{post-start}") : -len("#{post-end}")]

    count_matches = re.findall(r":[0-9]+", raw_block)

    if not count_matches:
        return raw_block, 9999

    return raw_block.replace(count_matches[0], ""), int(count_matches[0][1:])


def _expand_post_blocks(content: str) -> str:
    """
    Expands post blocks.
    """

    start_location = content.find("#{post-start}")
    stop_location = content.find("#{post-end}") + len("#{post-end}")
    if start_location == -1 or stop_location == -1:
        return content

    above_content = content[:start_location]
    below_content = content[stop_location:]
    block, count = _clean_block(content[start_location:stop_location])

    content = above_content
    for post_spec in post_specs()[:count]:
        content += post_spec.transform(block)
    content += below_content

    return content


@lru_cache(maxsize=None)
def blog_pages() -> List[pages.Page]:
    """
    Returns correctly expanded blog pages.
    """

    logger.log().info("Expanding blog specific load in blog load.")

    return [
        pages.Page(url=page.url, content=_expand_post_blocks(page.content)) for page in pages.load(blog_pages=True)
    ]


@lru_cache(maxsize=None)
def post_pages() -> List[pages.Page]:
    """
    Returns post pages.
    """

    logger.log().info("Generating post load.")

    return [
        pages.Page(url=post_spec.url, content=post_spec.transform(post_spec.template.content))
        for post_spec in post_specs()
    ]
