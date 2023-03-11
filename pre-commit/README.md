# pre-commit-hooks for python projects
usecase: performs automated code style checks on a python git repository

## install pre-commit
`pip3 install pre-commit`

## setup your repo
copy `.pre-commit-config.yaml` and `setup.cfg` to your git repo

## run manually
`pre-commit run -a`
or
`pre-commit run --files myFile1.py myFile2.py`

## run automatically via github actions
copy dir `.github/workflows/` to your repo, to automatically run upon push of commits and creation of pull requests.

## configure
* `.pre-commit-config.yaml` define which hooks to run
* `setup.cfg` sets flake8 parameters to use

## update pre-commit hooks to latest version
run `pre-commit autoupdate` to update hook versions in `.pre-commit-config.yaml`
