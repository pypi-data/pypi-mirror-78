"""
Implements types and functions relating to PyBlog's variables.
"""

from functools import lru_cache
from typing import List, NamedTuple, Union

import yaml

from ochs import logger, settings


class Variable(NamedTuple):
    """
    A blog templating variable.
    """

    name: str
    value: str

    def transform(self, content: str) -> str:
        """
        Expands occurrences of the variable in a string.
        """

        return content.replace(f"@{{{self.name}}}", self.value)


@lru_cache(maxsize=None)
def load() -> List[Variable]:
    """
    Loads the variables.
    """

    logger.log().info("Loading load.")

    with open(settings.variables_path(), "r") as file:
        content = yaml.safe_load(file)

    return [Variable(**raw_variable) for raw_variable in content]


def expand(content: str, variables: Union[None, List[Variable]] = None) -> str:
    """
    Transforms variable names in a string into their respective values.
    """

    if variables is None:
        variables = load()

    for variable in variables:
        content = variable.transform(content)

    return content
