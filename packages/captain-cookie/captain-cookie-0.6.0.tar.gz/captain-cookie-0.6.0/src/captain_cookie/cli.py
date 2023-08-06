""" A simple command line interface wrapper around cookiecutter which uses the template defined in this project. """
from pathlib import Path
import sys

from cookiecutter.main import cookiecutter


TEMPLATES_DIRECTORY = Path(__file__).parent / "templates"


def run(template: str = "default") -> None:
    """ Generate a new project using given template """
    template_path = TEMPLATES_DIRECTORY / template
    if not template_path.is_dir():
        print(f"Template not found: {template}", file=sys.stderr)
        sys.exit(1)
    print(f"Creating new project using captain-cookie {template} template.\n")
    cookiecutter(str(template_path))
