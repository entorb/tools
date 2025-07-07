#!/bin/bash

# edit git history
# combine all changes on certain files into a single commit

# pip install git-filter-repo

REPO=analyze-activities
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
    # .github
    # .vscode
    # .gitattributes
    # .gitignore
    # .pre-commit-config.yaml
    # .python-version
    # cspell-words.txt
    # cspell.config.yaml
    README.md
    # ruff.toml
    # sonar-project.properties
)

# filter out not existing files and dirs from $FILES
EXISTING_FILES=()
for FILE in "${FILES[@]}"; do
    if [ -e "$FILE" ]; then
        EXISTING_FILES+=("$FILE")
    else
        echo "WARN: $FILE not existing"
    fi
done
FILES=("${EXISTING_FILES[@]}")

for FILE in "${FILES[@]}"; do
    cp -r $FILE $BACKUP/
done

CMD="git-filter-repo --prune-empty always --invert-paths"
for FILE in "${FILES[@]}"; do
    CMD="$CMD --path $FILE"
done
echo $CMD
read -p "Enter to resume ..."
eval $CMD

# restore .git/config
cp $BACKUP/config .git/

# restore FILES
for FILE in "${FILES[@]}"; do
    cp -r $BACKUP/$FILE ./
done

git status
MSG="README, cspell, gitignore, pre-commit"
echo commit: $MSG
read -p "Enter to resume ..."
git add .
git commit -m $MSG

read -p "Enter to force push ..."
git push -f

rm -rf $BACKUP
rm -rf $DIR
