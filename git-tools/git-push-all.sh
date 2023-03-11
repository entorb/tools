#!/bin/bash

for D in `ls -d */`
do
    echo ===
    echo === $D ====
    echo ===
    cd $D
    git add .
    git commit -m "chmod u+x"
    git push
    cd ..
done
