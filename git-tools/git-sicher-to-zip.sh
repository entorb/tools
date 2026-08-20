#!/bin/sh

set -eu

TIMESTAMP=$(date +%y%m%d-%H%M)
OUT="GitHub-${TIMESTAMP}.zip"

rm -f "$OUT"

find . \
  \( -path "*/.git" \
  -o -path "*/.venv" \
  -o -path "*/node_modules" \
  -o -path "*/__pycache__" \
  -o -path "*/.rumdl_cache" \
  -o -path "*/.ruff_cache" \
  -o -path "./zzz*" \
  -o -path "./private/Python/mp3-streaming-renamer/audacity" \
  -o -path "./GitHub-*.zip" \
  \) -prune -o \
  -type f \
  ! -name "*.pyc" \
  ! -name ".DS_Store" \
  ! -name "$OUT" \
  ! -size +1M \
  -print >/tmp/ziplist.$$

zip -X -@ "$OUT" </tmp/ziplist.$$
rm -f /tmp/ziplist.$$

echo "Created: $(pwd)/$OUT"
