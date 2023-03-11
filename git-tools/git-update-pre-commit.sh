#!/bin/bash

FILE=".pre-commit-config.yaml"

for D in $(ls -d */); do
    if [ $D == 'hpmor-en/' ]; then
        echo skipping $D
        continue
    fi
    cd $D
    if [ -f $FILE ]; then
        echo $D
        cp ../tools/pre-commit/$FILE ./$FILE
    fi
    cd ..
done
