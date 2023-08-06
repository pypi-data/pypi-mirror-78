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

from ochs import logger, pages, settings, templates, variables


def _suffix_format(dt: date) -> str:
    """
    Special format for day suffix. I.e., th for 13, st for 1, or nd for 2.
    """

    if 4 <= dt.day <= 20 or 24 <= dt.day <= 30:
        return "th"

    SUFFIX_RULE = {1: "st", 2: "nd", 3: "rd"}
    return SUFFIX_RULE[dt.day % 10]


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

        # Replace dates using special formatting rules
        date_instances = re.findall(r"#{post-date:[^}]+}", content)
        for date_instance in date_instances:
            date_format = date_instance[12:-1].replace("%$", _suffix_format(self.date))
            content = content.replace(date_instance, self.date.strftime(date_format))

        # Replace other variables
        return (
            content.replace("#{post-title}", self.title)
            .replace("#{post-author}", self.author)
            .replace("#{post-preview}", self.preview)
            .replace("#{post-content}", self.content)
            .replace("#{post-url}", self.url)
        )


def preprocess_markdown(content: str) -> str:
    """
    Pre-processes markdown content by adding code-blocks with appropriate language tags
    and expanding variables.
    """

    lines = content.splitlines(keepends=True)

    inside_code_block = False
    for index, line in enumerate(lines):
        if line.startswith("```"):
            if inside_code_block:
                lines[index] = "</code></pre>"
                inside_code_block = False
                continue

            lines[index] = f'<pre><code class="language-{line[3:-1]}">'
            inside_code_block = True
            continue

        if inside_code_block:
            lines[index] = line.replace("<", "&#60;").replace(">", "&#62;")

    return variables.expand("".join(lines)).replace(r"@\{", "@{").replace("#{", r"#\{")


def load_post_file(filename: str) -> str:
    """
    Loads a post file.
    """

    with open(os.path.join(settings.posts_folder(), filename), "r") as file:
        content = file.read()

    return markdown(preprocess_markdown(content))


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
        pages.Page(url=post_spec.url, content=post_spec.transform(post_spec.template.content).replace(r"#\{", "#{"))
        for post_spec in post_specs()
    ]
