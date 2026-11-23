#!/usr/bin/env bash
set -euo pipefail

# change commit date for all commits after a given commit SHA

SHA="5caece35c73c68389ff3866634bcaca3b1302785"
NEW_DATE="2026-10-11T12:34:56"

export NEW_DATE

git rev-parse --verify "$SHA^{commit}" >/dev/null

if ! git merge-base --is-ancestor "$SHA" HEAD; then
  echo "error: $SHA is not an ancestor of HEAD" >&2
  exit 1
fi

if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "error: working tree not clean" >&2
  exit 1
fi

FILTER_BRANCH_SQUELCH_WARNING=1 git filter-branch -f --env-filter '
  export GIT_AUTHOR_DATE="$NEW_DATE"
  export GIT_COMMITTER_DATE="$NEW_DATE"
' "$SHA"..HEAD

echo "Done. Commits after $SHA now dated $NEW_DATE."
