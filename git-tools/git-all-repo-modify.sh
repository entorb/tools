#!/bin/bash

# exit upon error
set -e

for D in */; do
  # skip dirs starting with zzz_ as well as hpmor-de/
  if [[ $D == zzz_*/ || $D == hpmor-de/ ]]; then
    continue
  fi

  echo "==="
  echo "=== $D ===="
  echo "==="
  cd "$D"

  # if [[ $(git status --porcelain) ]]; then
  #   git add .github/workflows/*.yml
  #   git commit -m "Update check.yml"
  #   git push
  # fi
  # ../git-hist-cleanup.py

  # ../git-squash-same-message.sh
  # git checkout main
  # git pull

  # git checkout -- cspell-words.txt
  # echo shfmt >>cspell-words.txt
  # prek run --all-files

  # if [ -f cspell.config.yaml ]; then
  #   # prek run --all-files || true
  #   prek run --all-files
  #   # pnpm dlx cspell-cli@10.0.1 --unique --words-only .
  #   # git add cspell.config.yaml
  #   # git commit -m "chore: cspell.config.yaml"
  # fi

  if [[ $(git status --porcelain) ]]; then
    FILE=.pre-commit-config.yaml
    if [ -f $FILE ]; then
      git add $FILE
      git commit -m "chore: pre-commit add gitleaks"
    fi
    git push
  fi

  # ../git-hist-cleanup.py
  # git add .pre-commit-config.yaml
  # git commit -m ".pre-commit-config.yaml"
  # git push

  # reset author
  # git rebase -r --root --exec 'git commit --amend --no-edit --author="Torben <59419684+entorb@users.noreply.github.com>"'
  # git push -f

  # revert changes to file
  # if [[ $(git status --porcelain) ]]; then
  #     git checkout -- pyproject.toml
  # fi

  # cp ../korrekturleser/scripts/chk_md_lint.sh scripts/
  # cp ../korrekturleser/scripts/chk_pre-commit.sh scripts/
  # cp ../korrekturleser/scripts/chk_spelling.sh scripts/
  # cp ../korrekturleser/scripts/run_checks.sh scripts/

  # if [[ $(git status --porcelain) ]]; then
  # add only if exist
  # for f in scripts .pre-commit-config.yaml cspell-words.txt; do
  # 	[ -f "$f" ] && git add "$f"
  # done
  # for f in scripts .pre-commit-config.yaml cspell-words.txt; do
  #   [ -d "$f" ] && git add "$f"
  # done
  # git commit -m "prek: add shfmt"
  # git push
  # fi

  # if [[ $(git status --porcelain) ]]; then
  #     git add ruff.toml
  #     git commit -m "ruff.toml"
  #     git push
  # fi

  # ensure for all Python repos ruff is in check.yml
  # if [ -f pyproject.toml ]; then
  # if ! grep -q "ruff" .github/workflows/check.yml; then
  #     echo "Error: 'ruff' not found in check.yml" >&2
  # fi
  # fi

  # FILE="cspell.config.yaml"
  # if [ ! -f $FILE ]; then
  # echo "MISSING $FILE"
  # fi

  # yaml lint via ryl
  # uvx ryl@0.21.0 check -d '{extends: default, rules: {line-length: disable, truthy: disable}, ignore: [pnpm-lock.yaml]}' . --fix
  # git add cspell.config.yaml .github/workflows/*.yml
  # git commit -m "yaml lint"
  # git push

  cd ..
done

# spell:words prek rumdl hpmor korrekturleser cooldown pyproject
