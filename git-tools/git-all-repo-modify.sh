#!/bin/bash

for D in $(ls -d */); do
    if [ $D == "zzz_other/" ]; then continue; fi
    if [ $D == "template-python/" ]; then continue; fi

    if [ $D == "hpmor-de/" ]; then continue; fi
    echo ===
    echo === $D ====
    echo ===
    cd $D
    git pull
    cp ../template-python/.gitattributes ./
    git add .gitattributes
    git commit -m "Update .gitattributes"
    git push

    # if [ ! -f LICENSE ]; then
    #     read -p "LICENSE missing, shall we add it? (y/n) " choice
    #     if [ "$choice" == "y" ]; then
    #         cp ../template-python/LICENSE ./
    #         git add LICENSE
    #         git commit -m "Add LICENSE file"
    #         git push
    #     fi
    # fi

    # if [ -f setup.cfg ]; then
    #     read -p "replace setup.cfg by .ruff.toml? (y/n) " choice
    #     if [ "$choice" == "y" ]; then
    #         cp ../template-python/.ruff.toml ./
    #         cp ../template-python/.pre-commit-config.yaml ./
    #         rm setup.cfg
    #         # git add .ruff.toml
    #         # git commit -m "Add .ruff.toml file"
    #         # git push
    #     fi
    # fi

    # if [ ! -f .pre-commit-config.yaml ]; then
    #     read -p "add .pre-commit-config.yaml? (y/n) " choice
    #     if [ "$choice" == "y" ]; then
    #         cp ../template-python/.ruff.toml ./
    #         cp ../template-python/.pre-commit-config.yaml ./
    #         # git add .ruff.toml
    #         # git commit -m "Add .ruff.toml file"
    #         # git push
    #     fi
    # fi
    cd ..
done