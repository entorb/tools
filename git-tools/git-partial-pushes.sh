#!/bin/bash

# 1. create empty backup repo in GitHub
# e.g. COVID-19-Coronavirus-German-Regions-OLD-DATA-BACKUP-220730.git

# 2. clone new backup repo
# git clone git@github.com:entorb/COVID-19-Coronavirus-German-Regions-OLD-DATA-BACKUP-220730.git
# copy source repo files to backup repo

# in case git push fails with
# remote: fatal: pack exceeds maximum allowed size (2.00 GiB)
# fatal: sha1 file '<stdout>' write error: Broken pipe77 MiB/s
# read
# https://stackoverflow.com/questions/15125862/github-remote-push-pack-size-exceeded
# and
# https://stackoverflow.com/questions/28417845/pushing-a-large-github-repo-fails-with-unable-to-push-to-unqualified-destinatio

# for initial push
git log --pretty=oneline --reverse | head -1
# 1a179e2db55c510aa4a682f89810199d47973b9b Initial commit

# for init

max=$(git log --oneline | wc -l)
for i in $(seq $max -100 1); do
    echo $i
    # cspell:disable-next-line
    g=$(git log --reverse --oneline --skip $i -n1 | perl -alne'print $F[0]')
    git push origin $g:refs/heads/master
done

#1 create
git log --oneline >../commit-hist.txt

# REM initial push (last line in commit-hist.txt)
# git push origin 1a179e2db5:refs/heads/master

# REM now a push every 500 commits
# git push origin 9cd38977e3:master
# git push origin 936fb36d62:master
# git push origin 5ffda7235d:master
# git push origin afee88ccc4:master
