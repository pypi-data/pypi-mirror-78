""" A dummy conftest to illustrate pytest configuration """

from pytest import fixture

from {{ cookiecutter.project_slug }} import __version__


@fixture
def version() -> str:
    """ Return the current version of the {{ cookiecutter.project_slug }} package """
    return __version__
