# {{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description }}

---

<a href="{{ cookiecutter.repo_url }}/-/commits/next"><img alt="Pipeline status" src="{{ cookiecutter.repo_url }}/badges/next/pipeline.svg"></a>
<a href="{{ cookiecutter.repo_url }}/-/commits/next"><img alt="Coverage report" src="{{ cookiecutter.repo_url }}/badges/next/coverage.svg"></a>
<a href="https://python-poetry.org/docs/"><img alt="Packaging: poetry" src="https://img.shields.io/badge/packaging-poetry-blueviolet"></a>
<a href="https://flake8.pycqa.org/en/latest/"><img alt="Style: flake8" src="https://img.shields.io/badge/style-flake8-ff69b4"></a>
<a href="https://black.readthedocs.io/en/stable/"><img alt="Format: black" src="https://img.shields.io/badge/format-black-black"></a>
<a href="https://docs.pytest.org/en/stable/"><img alt="Packaging: pytest" src="https://img.shields.io/badge/tests-pytest-yellowgreen"></a>
<a href="https://pypi.org/project/{{ cookiecutter.project_slug }}/"><img alt="PyPI" src="https://img.shields.io/pypi/v/{{ cookiecutter.project_slug }}"></a>
<a href="{{ cookiecutter.docs_url }}"><img alt="Documentation" src="https://img.shields.io/badge/docs-mkdocs-blue"></a>

---

## Introduction

> TODO: Write a few words about the package here

## Quick start

> TODO: Quick presentation of packkage usage

### Installing the package

> TODO: Explain installation procedure

This package is not (yet?) distributed on [pypi](https://pypi.org/). As such it cannot be installed directly using pip.

You can however install it from the git repository directly using SSH credentials:

- Using [pip](https://pip.pypa.io/en/stable/):

```bash
pip install git+{{ cookiecutter.repo_url }}
```

- Using [poetry](https://python-poetry.org/):

```bash
poetry add git+{{ cookiecutter.repo_url }}
```

### Using the package

> TODO: Show more advanced usages

## Contributing

> TODO: Tell fellow developpers how to contribute to the package.

1. First clone the repository

```bash
git clone {{ cookiecutter.repo_url }}
```

2. Install the package

This project relies on the dependency manager [poetry](https://python-poetry.org/). Make sure it is installed then go into the project directory and install the package:

```bash
poetry install
```

3. Serve the documentation and check the contribution guide :smile:

```bash
poetry shell
mkdocs serve
```
