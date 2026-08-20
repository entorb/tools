#!/usr/bin/env bash
# squash-same-message.sh
#
# Squashes ADJACENT commits on the current branch that share the exact
# same commit message (subject line) into one commit each.
#
# SCOPE controls how far back it looks:
#   "unpublished" - only commits not yet pushed (origin/main..HEAD)
#   "all"         - every commit on the branch (root..HEAD)

set -euo pipefail

SCOPE="all" # "unpublished" or "all"

if [ "$SCOPE" = "all" ]; then
	range="HEAD"
	rebase_target=(--root)
else
	base_sha=$(git rev-parse origin/main)
	range="$base_sha..HEAD"
	rebase_target=("$base_sha")
fi

commits=()
while IFS= read -r sha; do
	commits+=("$sha")
done < <(git rev-list --reverse "$range")

todo_file=$(mktemp)
trap 'rm -f "$todo_file"' EXIT

: >"$todo_file"
prev_msg=""

for sha in "${commits[@]}"; do
	msg=$(git log -1 --format=%s "$sha")
	short=$(git rev-parse --short "$sha")
	if [ "$msg" = "$prev_msg" ]; then
		echo "fixup $short $msg" >>"$todo_file"
	else
		echo "pick $short $msg" >>"$todo_file"
	fi
	prev_msg="$msg"
done

GIT_SEQUENCE_EDITOR="cp '$todo_file'" git rebase -i "${rebase_target[@]}"
