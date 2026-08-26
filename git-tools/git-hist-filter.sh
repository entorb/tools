#!/bin/bash
#
# run this from the root of the git repo you want to filter
#
# uses git-filter-repo to remove files/dirs from git history
# pip install git-filter-repo
#

set -euo pipefail

FILES=(
  git-tools
)

DIR_CLONE="/tmp/git-filter-repo-clone"
DIR_CLONE_BACKUP="/tmp/git-filter-repo-backup"
DIR_BACKUP_ZIP=~/GitHub/zzz_backup

[[ -d .git ]] || {
  echo "Error: current directory is not the root of a git repo" >&2
  exit 1
}

DIR_LOCAL_REPO=$(pwd)
REPO=$(basename "$DIR_LOCAL_REPO")
REMOTE_URL=$(git remote get-url origin) || {
  echo "Error: repo $REPO has no 'origin' remote" >&2
  exit 1
}

rm -rf "$DIR_CLONE"
rm -rf "$DIR_CLONE_BACKUP"

cleanup() {
  local status=$?
  rm -rf "$DIR_CLONE" "$DIR_CLONE_BACKUP"
  if [[ $status -ne 0 ]]; then
    echo "Aborted (exit $status) — temp dirs cleaned up, nothing pushed unless you saw 'git push' succeed above." >&2
  fi
  exit $status
}
trap cleanup EXIT INT TERM

mkdir -p "$DIR_CLONE" "$DIR_CLONE_BACKUP"

cd "$DIR_CLONE"
git clone "$REMOTE_URL" "$REPO"
cd "$REPO"

DATE=$(date +"%y%m%d_%H%M%S")
echo "zipping to $DIR_BACKUP_ZIP/$REPO-$DATE.zip"
mkdir -p "$DIR_BACKUP_ZIP"
zip -r9q "$DIR_BACKUP_ZIP/$REPO-$DATE.zip" . -x '.git/*'

# backup .git/config
cp .git/config "$DIR_CLONE_BACKUP/config"

ARGS=(--prune-empty always --invert-paths)
for FILE in "${FILES[@]}"; do
  ARGS+=(--path "$FILE")
done

echo "git-filter-repo ${ARGS[*]}"
# read -r -p "Enter to filter the repo $REPO history ..."
git-filter-repo "${ARGS[@]}"

# restore .git/config
cp "$DIR_CLONE_BACKUP/config" .git/

# Explicit cleanup (git-filter-repo usually does this already)
git reflog expire --expire=now --all
git gc --prune=now

if [[ $(git status --porcelain) ]]; then
  git status
fi

# read -r -p "Enter to force push and pull local repo..."
git push -f

cd "$DIR_LOCAL_REPO"
git fetch origin
git reset --hard origin/main

echo "Done."
