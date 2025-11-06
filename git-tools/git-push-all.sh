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
    git add .
    git commit -m "chmod 744"
    git push
    cd ..
done
