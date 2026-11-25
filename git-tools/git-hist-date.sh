#!/usr/bin/env bash
set -euo pipefail

# Change commit dates for all commits after a given commit SHA.
# Usage: ./redate.sh [SHA] [NEW_DATE]
#   SHA       defaults to the value below
#   NEW_DATE  ISO 8601 (e.g. 2026-11-24T12:27:00) or "NOW" (default)

DEFAULT_SHA="d231223938087771d6767363b9837192c21b9ad6"

SHA="${1:-$DEFAULT_SHA}"
NEW_DATE="${2:-NOW}"

if [[ "$NEW_DATE" == "NOW" ]]; then
  NEW_DATE="$(date +%Y-%m-%dT%H:%M:%S)"
fi

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
