#!/bin/bash
set -e
# shellcheck disable=SC2103

for D in */; do
  # skip dirs starting with zzz_
  case $D in
    zzz_*) continue ;;
  esac
  echo "==="
  echo "=== $D ===="
  echo "==="
  cd "$D"
  git fetch origin
  git reset --hard origin/main
  git pull
  cd ..
done
