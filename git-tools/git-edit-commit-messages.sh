#!/usr/bin/env bash
#
# rewrite-commit-messages.sh
#
# Clones github.com/entorb/<repo> to /tmp/<repo>, exports a list of
# "<hash> <subject>" for you to hand-edit, then replays your edited
# subjects onto history with git filter-repo. Commit bodies are
# dropped; only the subject line survives.
#
# Usage:
#   ./rewrite-commit-messages.sh <repo-name>
#
# Example:
#   ./rewrite-commit-messages.sh flashcards
#

# LLM instruction:
# Improve the commit messages of this mono repo, containing the apps: 1x1, div, pum, voc, eta, lwk.
# use type prefixes in this format
# "<sha> <type>(<app>): <description>"
# type: feat (feature), fix (bugfix), docs, style (code format), refactor, perf (performance), test, chore (tooling, deps, build config, CI/CD config)
# app: optional and can be more than one of (1x1, div, pum, voc, eta, lwk)
# description: harmonize, improve, keep short, start with capital letter

set -euo pipefail

NAME="${1:?Usage: $0 <repo-name>  (e.g. flashcards, for github.com/entorb/flashcards)}"
SOURCE="https://github.com/entorb/${NAME}.git"
WORKDIR="/tmp/${NAME}"
MESSAGES_FILE="/tmp/${NAME}-messages.txt"
CALLBACK_FILE="/tmp/${NAME}-callback.py"

echo "## Removing $WORKDIR if it exists"
rm -rf "$WORKDIR"

echo "## Cloning $SOURCE to $WORKDIR"
git clone "$SOURCE" "$WORKDIR"
cd "$WORKDIR"

echo "## Exporting commit list to $MESSAGES_FILE"
git log --reverse --format='%H %s' >"$MESSAGES_FILE"

echo
echo "## Now edit the messages file:"
echo "    $MESSAGES_FILE"
echo
echo "    Each line is '<hash> <subject>'. Edit the text after each hash."
echo "    Do NOT touch the hashes. Commit bodies will be dropped."
echo
read -rp "Press Enter once you've saved your edits and are ready to rewrite history... "

echo "## Writing filter-repo callback to $CALLBACK_FILE"
cat >"$CALLBACK_FILE" <<PYEOF
mapping = {}
with open("${MESSAGES_FILE}", "rb") as f:
    for line in f:
        line = line.rstrip(b"\n")
        if not line.strip():
            continue
        hash_, msg = line.split(b" ", 1)
        mapping[hash_.strip()] = msg.strip()

if commit.original_id in mapping:
    commit.message = mapping[commit.original_id] + b"\n"
PYEOF

echo "## Running git filter-repo"
git filter-repo --commit-callback "$(cat "$CALLBACK_FILE")" --force

echo "## Re-adding origin remote (filter-repo strips it by default)"
git remote add origin "$SOURCE" || true

echo
echo "Done. Repo rewritten at: $WORKDIR"
echo "Review the log with: git -C \"$WORKDIR\" log --oneline"
echo "When happy, push with: git -C \"$WORKDIR\" push --force-with-lease"
