# pre-commit-hooks for python projects

usecase: performs automated code style checks on a python git repository
see <https://pre-commit.com> for details.

## install pre-commit

`pip3 install pre-commit`

## configure

copy and adjust `.pre-commit-config.yaml` and `.flake8` to your git repo

* `.pre-commit-config.yaml` defines which hooks to run, see <https://pre-commit.com/hooks.html> for complete list
* `.flake8` sets flake8 parameters to use

## update pre-commit hooks to latest version

`pre-commit autoupdate` to versions of all hooks in `.pre-commit-config.yaml`

## run automated as pre-commit hook in your local git repository

so it will be executed upon each local `git commit` command

`pre-commit install`

## run manually

check all files: `pre-commit run --all-files`
or
check certain files `pre-commit run --files myFile1.py myFile2.py`

## run automated via GitHub Actions

copy dir `.github/workflows/` to your repo, to automatically run upon push of commits and creation of pull requests.
