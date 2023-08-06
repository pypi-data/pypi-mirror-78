#!/usr/bin/env python
"""Hooks ran before project generation:

- validate_project_slug: Ensure that project_slug is a valid python module name
"""
import re
import sys


MODULE_REGEX = r"^[_a-zA-Z][_a-zA-Z0-9]+$"
MODULE_NAME: str = "{{ cookiecutter.project_slug}}"


def validate_project_slug(name: str) -> None:
    """Ensure that project slug is a valid python module name."""
    if not re.match(MODULE_REGEX, name):
        print(
            f"ERROR: The project slug {name} is not a valid Python module name."
            "Please do not use a - and use _ instead",
            file=sys.stderr)
        #Exit to cancel project
        sys.exit(1)

if __name__ == "__main__":

    validate_project_slug(MODULE_NAME)
