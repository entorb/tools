#!/bin/bash

# exit upon error
# set -e

for D in */; do
  # skip dirs starting with zzz_ as well as hpmor-de/
  case $D in
    zzz_*/ | hpmor-de/) continue ;;
  esac

  echo "==="
  echo "=== $D ===="
  echo "==="
  cd "$D"

  # ../git-squash-same-message.sh

  # git checkout main
  # git pull

  # git checkout -- cspell-words.txt
  # echo shfmt >>cspell-words.txt
  # prek run --all-files

  git add prek.toml
  git commit -m "prek.toml"
  git push

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
  # for f in scripts prek.toml cspell-words.txt; do
  # 	[ -f "$f" ] && git add "$f"
  # done
  # for f in scripts prek.toml cspell-words.txt; do
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

  #. ensure rumdl is in cspell-words.txt
  # if ! grep -q "rumdl" cspell-words.txt; then
  #     echo rumdl >> cspell-words.txt
  #     prek run --files cspell-words.txt
  #     git add cspell-words.txt
  #     git commit -m "cspell-words.txt"
  #     git push
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

  # if [ -f requirements.txt ]; then
  # if [ ! -f pyproject.toml ]; then
  # echo "USING PIP INSTEAD OF UV"
  # fi
  # fi

  # prek run --all-files
  # prek util yaml-to-toml
  # if [ -f scripts/chk_spelling.sh ]; then
  # if [[ $(git status --porcelain) ]]; then
  #     git add scripts/chk_spelling.sh
  #     git commit -m "scripts/chk_spelling.sh"
  #     git push
  # fi
  # fi

  # ensure git leaks in prek.toml
  # if ! grep -q "gitleaks" prek.toml; then
  #     echo "Error: 'gitleaks' not found in prek.toml" >&2
  #     exit 1
  # fi

  # add all spelling issues to dictionary
  # if [ -f cspell.config.yaml ]; then
  #     pnpm dlx cspell-cli@10.0.1 --unique --words-only . > cspell-words-missing.txt
  #     cat cspell-words-missing.txt >> cspell-words.txt
  #     prek run --all-files
  #     if [[ $(git status --porcelain) ]]; then
  #     git add cspell-words.txt
  #     git commit -m "cspell-words.txt"
  #     git push
  #     fi
  # fi

  # git add .github/*
  # git commit -m "Dependabot: action updates"
  # git push

  # git add .gitattributes
  # git commit -m ".gitattributes V2"
  # git push

  # git add .github/workflows/*.yml
  # git commit -m "Update check.yml"
  # git push

  # if [ -f .github/dependabot.yml ]; then
  #     git add .github/dependabot.yml
  #     git commit -m "dependabot cooldown"
  #     git push
  # fi

  # add only if exist
  # for f in .github/workflows/check.yml .github/workflows/update.yml .github/dependabot.yml pnpm-workspace.yaml; do
  #     [ -f "$f" ] && git add "$f"
  # done
  # if [[ $(git status --porcelain) ]]; then
  #     git commit -m "yml lint"
  #     git push
  # fi

  #     read -p "add .github/workflows (y/n) " choice
  #     if [ "$choice" == "y" ]; then
  #         mkdir -p .github/workflows
  #         cp ../template/python/.github/workflows/check.yml
  #     fi
  # fi

  # if [ ! -d .github ]; then
  #     read -p "add .pre-commit-config.yaml? (y/n) " choice
  #     if [ "$choice" == "y" ]; then
  #         cp ../template-python/ruff.toml ./
  #         cp ../template-python/.pre-commit-config.yaml ./
  #         # git add ruff.toml
  #         # git commit -m "Add ruff.toml file"
  #         # git push
  #     fi
  # fi

  cd ..
done

# spell:words prek rumdl hpmor korrekturleser cooldown pyproject
