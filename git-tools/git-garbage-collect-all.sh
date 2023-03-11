#!/bin/bash

for D in $(ls -d */); do
    echo ===
    echo === $D ====
    echo ===
    cd $D
    git reflog expire --expire=now --all
    git gc --prune=now --aggressive
    cd ..
done
