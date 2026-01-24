#!/bin/bash

# exit upon error
set -e

for D in */; do
    # skip dirs starting with zzz_ as well as hpmor-de/
    case $D in
        zzz_*/|hpmor-de/) continue ;;
    esac

    echo ===
    echo === $D ====
    echo ===
    cd $D
    git checkout main
    git pull
    # if [ -f .pre-commit-config.yaml ]; then
    #     pre-commit autoupdate
    #     pre-commit run --all-files
    #     git status
    #     # read -p "commit changes? (y/n) " choice
    #     # if [ "$choice" == "y" ]; then
    #     git add .pre-commit-config.yaml
    #     git commit -m "Update .pre-commit-config.yaml"
    #     git push
    #     # fi
    # fi


    # git add .github/workflows/*.yml
    # git commit -m "GH Action sonarqube-scan-action@v7"
    # git push

    git add *.sh
    git commit -m "Alignment deploy.sh update.sh"
    git push

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
