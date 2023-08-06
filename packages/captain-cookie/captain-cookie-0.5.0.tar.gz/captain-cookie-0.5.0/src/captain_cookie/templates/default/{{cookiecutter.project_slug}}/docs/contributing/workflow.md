# The development workflow

This documents can be used as a guideline when contributing to the project

## Create an issue

Before starting to write code, contributors are encouraged to open an issue on the GitLab repository that details either the problem that they want to fix or the feature that they want to add.

!!! warning "Avoid duplicate issues"
    There might be someone who already created a similar issue. Search the open and closed issues to make sure that no duplicate issues are created.


## Create a merge request and a branch

Once you confirmed that no issue existed for the problem you want to tackle, use GitLab to create a Merge Request and a branch associated with your issue.

!!! note "Avoid manually creating branches and merge request"
    This could be done easily using the command line, but using GitLab provides a better experience as issues, merge requests and branches are automatically linked.
    Moreover, branches and merge requests are automatically named based on the title of the issue so everything is consistent and easy to search.


## Fetch the newly created branch on your local repository

Use git to fetch the branch GitLab created for you:

```bash
git fetch
```

Once the branch has been fetched, you can start working on it:

```bash
git checkout <new_branch>
```

## Activate your virtual environment

If that was not already the case, make sure your virtual environment is activated:

```bash
python -m poetry shell
```

!!! note
    This command is just a convenient and portable way to run `. venv/bin/activate` on Linux or `.venv/Scripts/activate` on Windows.
    The main difference is that it spawns a new shell instead of modifying current shell environment.
    You should always enable your environment before writing code or serving the doc.


## Write unit tests for your code

When possible, write your unit tests before starting developping and writing some code. This will ensure the highest code coverage with minimal efforts.

If you are not familiar with test driven development, you can still write your code first and then write your unit tests. What matters is that new contributions are always shipped with tests and that code coverage does not decrease with new contributions.


## Write some code

When writing code, you must follow PEP8 recommendations. In order to ease the development process several tools are used:

- Flake8 is used to lint the code and ensure code quality.

- Black is used to format the code according to PEP8 recommendations

- Isort is used to ensure libraries imports follow PEP8 recommendations

Contributors are encouraged to heavily use those 3 tools when developping. The suggested VSCode configuration provides seamless integration with black and flake8.

If you want to use those tools, we provide invoke tasks:

- Lint your code:

```bash
invoke lint
```

- Format your code:

```bash
invoke format
```


### Type your code

- Always specify type of your functions arguments and outputs.

### Write docstrings

Docstrings will be used to automatically generate the API Documentation.

- Always write a docstring when declaring functions, classes or methods.
- Always write a docstring a the top of a module.


## Update the documentation

The API documentation is generated automatically from the types and docstrings but the user documentation must be maintained by the contributors.
When adding or modifying an existing feature, always update the user documentation accordingly

When updating the documentation, it is nice to run the mkdocs development server to see live changes. This can be done running the task `doc`:

```bash
invoke doc
```

## Commit your code and push your branch

Each time you feel that you achieved even a small milestone in the resolution of the issue you created, commit and your code and push your branch to GitLab repository.

Always make sure you're up to date with master branch and rebase your branch when it's not the case:

```bash
git rebase origin/master
```

!!! note
    If your project uses a develop branch, then rebase on the develop branch.

## Ask for review

Once you estimate that your contribution is ready to be reviewed, ask other contributors to review your merge request.

GitLab provides a really nice interface for code review and let users write comments or ask for modifications.

## :rocket: Merge the code

As soon as the contribution has been reviewed positively, ask a maintainer to merge your branch.

This should always be done using GitLab from the Merge Request interface.

!!! note
    To perform merge request, resolve the `WIP` status on the merge request, enable commit squashing and perform the merge or let the branch merge automatically when its CI pipeline is successfull.

Accepting the merge request will close the associated issue.
