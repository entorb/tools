#!/bin/bash

# edit git history
# combine all changes on certain files into a single commit

# pip install git-filter-repo
# cspell:disable-next-line
REPO=meeting-meter
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

MSG="Tools"
FILES=(
    .editorconfig
    .github
    .pre-commit-config.yaml
    .prettierignore
    .prettierrc.json
    .sonarcloud.properties
    .vscode
    cspell.config.yaml
    cspell.json
    eslint.config.ts
    ruff.toml
    sonar-project.properties
)

# MSG="README cspell gitignore"
# FILES=(
#     .gitignore
#     cspell-words.txt
#     deployment.md
#     README.md
# )

# MSG="Scripts"
# FILES=(scripts)

# MSG="Lock"
# FILES=(
#     package-lock.json
#     pnpm-lock.yaml
#     uv.lock
# )

# MSG="Packages"
# FILES=(
#     package.json
#     pyproject.toml
#     requirements-dev.txt
#     requirements.txt
# )

# MSG="Cypress"
# FILES=(
#     cypress
#     cypress.config.ts
# )

# MSG="AI-Tools"
# FILES=(
#     .claude
#     .gemini
#     CLAUDE.md
#     GEMINI.md
# )

for FILE in "${FILES[@]}"; do
    if [ -e "$FILE" ]; then
    cp -r $FILE $BACKUP/
    fi
done

CMD="git-filter-repo --prune-empty always --invert-paths"
for FILE in "${FILES[@]}"; do
    CMD="$CMD --path $FILE"
done
echo "->" $CMD
read -p "Enter to run fit-filter-repo ..."
eval $CMD

# restore .git/config
cp $BACKUP/config .git/

# restore FILES
for FILE in "${FILES[@]}"; do
    if [ -e "$BACKUP/$FILE" ]; then
    cp -r $BACKUP/$FILE ./
    fi
done

git status
echo "->" commit message: "$MSG"
read -p "Enter to commit ..."
git add .
git commit -m "$MSG"

echo "-> reflog expire & gc"
git reflog expire --expire=now --all
git gc --prune=now --aggressive

read -p "Enter to force push ..."
git push -f

echo "-> cleaning up"
cd /tmp
rm -rf $BACKUP
rm -rf $DIR

echo "->" now run  git fetch origin \& git reset --hard origin/main  on in your repo.
