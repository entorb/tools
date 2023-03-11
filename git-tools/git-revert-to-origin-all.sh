#!/bin/bash

for D in $(ls -d */); do
    echo ===
    echo === $D ====
    echo ===
    cd $D
    git fetch origin
    git reset --hard origin/main
    git pull
    cd ..
done
