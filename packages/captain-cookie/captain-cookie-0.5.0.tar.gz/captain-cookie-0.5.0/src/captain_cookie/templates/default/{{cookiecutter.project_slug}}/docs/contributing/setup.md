# Setting up the development environment

## Prerequisites


### Install Python version 3.7.X or 3.8.X

- You can install python on Windows using chocolatey

- You can install python on Linux systems using your package manager

### Install poetry

Even if it is not encouraged, the simplest way to install poetry is to use `pip`:

```bash
python -m pip install --user poetry
```

!!! note "Learn how to use poetry"
    Poetry is a powerful dependency management tool but can do much more than tracking dependencies. Take a look at the documentation
    to learn all its features: <https://python-poetry.org/docs/>

### Configure poetry

By default poetry creates virtual environments in user home directory when installing a package, but we want to install the environments inside the project.
This can be configured using the following command:

```bash
python -m poetry config virtualenvs.in-project true
```

## Installation

### Clone the repository

!!! note
    You must have git installed on your system

Once python and poetry are installed, you can clone the repository in the directory of your choice:

```bash
git clone {{ cookiecutter.repo_url }}
```

### Install the package using poetry

Go into the cloned directory and install it using poetry:

```bash
cd extractor/
python -m poetry install
```

!!! note
    This command creates a virtual environment named `.venv` in your repository if poetry is configured correctly.
    It also installs all development dependencies as well as main dependencies.
    Finally it installs the package in editable/development mode for those familiar with pip or setuptools.


## Configure VSCode

We recommend using VSCode IDE.

The following settings are recommended:

```json
{
  "files.exclude": {
    "**/.git": true,
    "**/.svn": true,
    "**/.hg": true,
    "**/CVS": true,
    "**/.DS_Store": true,
    ".hypothesis": true,
    ".mypy_cache": true,
    ".pytest_cache": true,
    ".venv/": true,
    ".coverage": true,
    "**/__pycache__/": true,
    "**/*.egg-info/": true
  },
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.linting.pylintEnabled": false,
  "editor.formatOnPaste": true,
  "editor.formatOnSave": true,
  // On windows
  "python.pythonPath": ".venv\\Scripts\\python.exe"
  // On linux
  // "python.pythonPath": ".venv/bin/python"
}
```

You can adapt them to your needs.

!!! note
    VSCode settings should be placed inside a file named `settings.json` inside a directory `.vscode` located at the root of the project.


## Install the pre-commit hooks

[pre-commit](https://pre-commit.com/) is used to ensure some tasks are always executed before commiting to the git repository.
It must be installed after cloning the project for the first time.

```bash
pre-commit install
```

!!! note "Customize your pre-commit hooks"
    Pre-commit is configured in the file `.pre-commit-config.yaml` at the root of the repository.
    You can add or remove tasks as you wish.
