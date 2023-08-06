#!/usr/bin/env python
"""Hooks ran after project generation."""
from pathlib import Path
from shutil import rmtree
from subprocess import check_call
import sys
from distutils.util import strtobool


def init_git() -> None:
    """Init a git repository."""
    try:
        check_call(["git", "init"])
        check_call(["git", "checkout", "-b", "next"])
    except Exception:
        print("Error encountered during 'git init' post install hook. Do you have git installed ?", file=sys.stderr)
        sys.exit(1)


def install_precommit() -> None:
    """Install pre-commit hooks."""
    try:
        check_call(["poetry", "run", "pre-commit", "install"])
    except Exception:
        print("Error encountered during 'pre-commit' post-install hook", file=sys.stderr)
        sys.exit(1)


def first_commit() -> None:
    """Commit after repository has been generated successfully."""
    try:
        check_call(["poetry", "run", "git", "add", "."])
        check_call(["poetry", "run", "git", "commit", "-m", "first commit"])
    except Exception:
        print("Error encountered during 'git commit' post-install hook.", file=sys.stderr)
        sys.exit(1)


def install_package() -> None:
    """Install package using poetry."""
    try:
        check_call(["poetry", "install"])
    except Exception:
        print("Error encountered during 'poetry install' post-install hook.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    init_git()
    install_package()
    install_precommit()
    first_commit()
