#!/bin/bash

# edit git history
# combine all changes on certain files into a single commit

# Works for files (1.txt), dirs (data), subdirectory paths (src/1.txt, apps/1x1/README.md), and globs (apps/*/README.md)

# pip install git-filter-repo
REPO=flashcards
DIR=/tmp/git-filter-repo-clone/
BACKUP=/tmp/git-filter-repo-backup

cd /tmp
mkdir -p $DIR
mkdir -p $BACKUP

cd $DIR
git clone git@github.com:entorb/$REPO.git
cd $REPO

# backup .git/config
cp .git/config $BACKUP/config

MSG="Documentation"
FILES=(
    AGENTS.md
    apps/*/AGENTS.md
    apps/*/README.md
    cspell-words.txt
    deployment.md
    packages/shared/AGENTS.md
    packages/shared/README.md
    README.md
    TODO.md
)

# MSG="Tools"
# FILES=(
#     .editorconfig
#     .github
#     .gitignore
#     .pre-commit-config.yaml
#     .prettierignore
#     .prettierrc.json
#     .sonarcloud.properties
#     .sonarlint
#     .vscode
#     cspell.config.yaml
#     cspell.json
#     eslint.config.ts
#     ruff.toml
#     sonar-project.properties
# )

# MSG="Scripts"
# FILES=(
#     scripts
#     apps/*/scripts
# )

# MSG="Lock"
# FILES=(
#     package-lock.json
#     pnpm-lock.yaml
#     uv.lock
# )

# MSG="Packages"
# FILES=(
#     package.json
#     apps/*/package.json
#     packages/shared/package.json
#     pyproject.toml
#     requirements-dev.txt
#     requirements.txt
# )

# MSG="Cypress"
# FILES=(
#     apps/*/cypress
#     apps/*/cypress.config.ts
#     cypress
#     cypress.config.ts
# )

# MSG="Vitest"
# FILES=(
#     apps/*/src/__tests__
#     packages/shared/src/__tests__
#     apps/wordplay/src/pages/HomePage.spec.ts
# )

# MSG="Icons"
# FILES=(
#     apps/*/assets/icon.svg
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
        # Preserve directory structure in backup
        mkdir -p "$BACKUP/$(dirname "$FILE")"
        cp -r "$FILE" "$BACKUP/$FILE"
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
        # Preserve directory structure when restoring
        mkdir -p "$(dirname "$FILE")"
        cp -r "$BACKUP/$FILE" "$FILE"
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

echo "->" now run
echo  git fetch origin \&\& git reset --hard origin/main
echo on in your repo.
