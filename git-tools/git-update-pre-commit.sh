#!/bin/bash

FILE=".pre-commit-config.yaml"

for D in $(ls -d */); do
    # skip dirs starting with zzz_
    case $D in
    zzz_*) continue ;;
    esac
    echo "=== $D ==="
    if [[ "$D" =~ ^(pre-commit-config/|hpmor-de/|private/|raspi-sensorics/|strava/|tools/|tools-photos/|typonuketool/)$ ]]; then
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
        cp ../pre-commit-config/$FILE ./$FILE
        cp ../pre-commit-config/.ruff.toml ./
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
