import tomllib
from typing import Any


def read_pyproject_toml() -> dict[str, Any]:
    """Reads the pyproject.toml file.

    :returns: The contents of the pyproject.toml file.
    :rtype: dict[str, Any]
    """
    with open('./pyproject.toml', 'rb') as file:
        return tomllib.load(file)
