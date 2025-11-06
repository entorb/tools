#!/bin/bash

for D in $(ls -d */); do
    # skip dirs starting with zzz_
    case $D in
    zzz_*) continue ;;
    esac
    echo ===
    echo === $D ====
    echo ===
    cd $D
    git reflog expire --expire=now --all
    git gc --prune=now --aggressive
    cd ..
done
