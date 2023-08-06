"""
Module handling templates.
"""

import os
import re
from functools import lru_cache
from typing import Dict, List, NamedTuple

import yaml

from ochs import logger, settings, variables


class TemplateSpec(NamedTuple):
    """
    Specification for a blog template.
    """

    name: str
    filename: str


class Template(NamedTuple):
    """
    A blog template.
    """

    name: str
    content: str


Templates = Dict[str, Template]


@lru_cache(maxsize=None)
def load_specs() -> List[TemplateSpec]:
    """
    Loads all the template specifications.
    """

    with open(settings.template_specs_path(), "r") as file:
        content = yaml.safe_load(file)

    return [TemplateSpec(**raw_spec) for raw_spec in content]


def _load_with_variables(spec: TemplateSpec) -> Template:
    """
    Loads a single template based on a specification, already expanding
    variables.
    """

    filepath = os.path.join(settings.templates_folder(), spec.filename)
    with open(filepath, "r") as file:
        content = file.read()

    return Template(name=spec.name, content=variables.expand(content))


def _find_required_expansions(template: Template) -> List[str]:
    """
    Returns a list with the names of the templates required for expanding the given template.
    """

    return [match[2:-1] for match in set(re.findall(r"\${[A-Za-z0-9\-_]+}", template.content))]


def _expand_template(to_expand: Template, expansion_source: Template) -> Template:
    """
    Expands a single template with another one.
    """

    return Template(
        name=to_expand.name,
        content=to_expand.content.replace(f"${{{expansion_source.name}}}", expansion_source.content),
    )


def _expand_with_other_templates(template: Template, templates_: Templates) -> Template:
    """
    Expands a template with the contents of other templates.
    """

    required_expansions = _find_required_expansions(template)
    for expansion in required_expansions:
        template = _expand_template(template, templates_[expansion])

    if _find_required_expansions(template):
        template = _expand_with_other_templates(template, templates_)

    return template


@lru_cache(maxsize=None)
def load() -> Templates:
    """
    Loads all the templates with all of its expansions.
    """

    logger.log().info("Loading load.")

    templates = dict()
    for spec in load_specs():
        templates[spec.name] = _load_with_variables(spec)

    for name, template in templates.items():
        templates[name] = _expand_with_other_templates(template, templates)

    return templates
