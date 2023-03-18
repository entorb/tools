#!/bin/bash

FILE=".pre-commit-config.yaml"

for D in $(ls -d */); do
    echo "=== $D ==="
    if [[ "$D" =~ ^(hpmor-en/|DukeTypem2D/)$ ]]; then
        echo skipping $D
        continue
    fi
    cd $D
    if [ -f $FILE ]; then
        # check for modifications
        if ! [ -z "$(git status --porcelain)" ]; then
            echo 'commit and push first'
            exit 1
        fi
        git pull
        cp ../tools/pre-commit/$FILE ./$FILE
        # if changes, run pre-commit and commit afterwards
        if ! [ -z "$(git status --porcelain)" ]; then
            pre-commit run -a || {
                echo 'pre-commit failed'
                exit 1
            }
            git status
            read -p "Press [Enter] to commit changes"
            git add .
            git commit -m "pre-commit update"
            git push || {
                echo 'push failed'
                exit 1
            }
        fi
    fi
    cd ..
done
