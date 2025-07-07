#!/bin/bash

# use git-filter-repo to remove files/dirs from git history

# pip install git-filter-repo

REPO=tools
DIR=/tmp/git-filter-repo-clone/
BACKUP=/tmp/git-filter-repo-backup

cd /tmp
mkdir $DIR
mkdir $BACKUP

cd $DIR
git clone git@github.com:entorb/$REPO.git
cd $REPO

# backup .git/config
cp .git/config $BACKUP/config

FILES=(
    sql2csv_postgresql.py
)

CMD="git-filter-repo --prune-empty always --invert-paths"
for FILE in "${FILES[@]}"; do
    CMD="$CMD --path \"$FILE\""
done
echo $CMD
read -p "Enter to resume ..."
eval $CMD

# restore .git/config
cp $BACKUP/config .git/

git status

read -p "Enter to force push ..."
git push -f

rm -rf $BACKUP
rm -rf $DIR
