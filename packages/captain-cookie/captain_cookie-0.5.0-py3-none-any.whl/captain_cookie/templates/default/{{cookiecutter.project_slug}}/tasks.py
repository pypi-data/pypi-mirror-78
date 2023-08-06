""" Tasks for {{ cookiecutter.project_slug }} project. """
import os
from pathlib import Path
from shutil import rmtree

from invoke import task

PROJECT_DIR = Path(__file__).parent

SRC_DIR = PROJECT_DIR / "src"
TESTS_DIR = PROJECT_DIR / "tests"
DIST_DIR = PROJECT_DIR / "dist"
DOCS_DIR = PROJECT_DIR / "docs"
DOCS_DIST_DIR = DIST_DIR / "docs"

SRC_FILES = " ".join([str(path) for path in SRC_DIR.glob("**/*.py")])
TEST_FILES = " ".join([str(path) for path in TESTS_DIR.glob("**/*.py")])


@task
def lint(c):
    """Lint the code sources."""
    c.run(f"flake8 {SRC_FILES} {TEST_FILES} tasks.py")


@task
def format(c):
    """Format the code sources."""
    c.run(f"black {SRC_FILES} {TEST_FILES} tasks.py")
    c.run(f"isort {SRC_FILES} {TEST_FILES} tasks.py")


@task
def test(c):
    """Run the unit tests."""
    c.run("pytest")


@task
def build(c, package=True, docs=True, coverage=True):
    """Build the user documentation."""
    if docs:
        c.run(f"mkdocs build -d {DOCS_DIST_DIR}")
        if coverage:
            if not Path(DOCS_DIR / "coverage-report" / "index.html").is_file():
                print("Running tests to generate coverage report.")
                c.run("pytest")
    if package:
        c.run("poetry build")


@task
def docs(c, coverage=True):
    """Serve the documentation."""
    if coverage:
        if not Path(DOCS_DIR / "coverage-report" / "index.html").is_file():
            print("Running tests to generate coverage report.")
            c.run("pytest")
    c.run("mkdocs serve")


@task
def publish(c, username=None, password=None):
    """Publish the package."""
    if username is None:
        username = os.environ["PYPI_USERNAME"]
    if password is None:
        password = os.environ["PYPI_PASSWORD"]
    c.run(f"poetry publish -u {username} -p {password}")


@task
def clean(c):
    """Clean the build artefacts."""
    try:
        rmtree(PROJECT_DIR / "dist")
    except FileNotFoundError:
        pass


@task
def build_ci_image(c, image="{{ cookiecutter.ci_docker_image }}"):
    """Build the Docker image for Continuous Integration."""
    c.run(f"docker build -t {image} -f ci/Dockerfile .")
