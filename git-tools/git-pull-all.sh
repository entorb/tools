#!/bin/bash

for D in `ls -d */`
do
    echo ===
    echo === $D ====
    echo ===
    cd $D
    git pull
    cd ..
done
