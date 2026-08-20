#!/bin/sh
# cspell:disable

set -eu

cd ~/GitHub

# cleanup
sh private/python-go-rust/cleanup.sh
sh hpmor-de/scripts/cleanup.sh
rm -f hpmor-de/*.pdf

TIMESTAMP=$(date +%y%m%d-%H%M)
OUT="GitHub-${TIMESTAMP}.tar.xz"

ZIPLIST=$(mktemp)
trap 'rm -f "$ZIPLIST"' EXIT

rm -f "$OUT"

find . \
  \( -path "OUT" \
  -o -path "./arduino-sensorics/libraries/ESP8266_Influxdb" \
  -o -path "./arduino-sensorics/libraries/MH-Z19" \
  -o -path "./arduino-sensorics/libraries/TM1637" \
  -o -path "./arduino-sensorics/libraries/U8g2" \
  -o -path "./GitHub-*.zip" \
  -o -path "./hpmor-de/fonts" \
  -o -path "./private/Python/adventskalenderlauf/*.png" \
  -o -path "./private/Python/CClicker-Bau/*.png" \
  -o -path "./private/Python/CClicker-Bau/templates/*.png" \
  -o -path "./private/Python/mp3-streaming-renamer/audacity" \
  -o -path "./private/xplanet/images" \
  -o -path "./rememberthemilk/cache" \
  -o -path "./strava/lib" \
  -o -path "./strava/tmp" \
  -o -path "./zzz*" \
  -o -path "*/__pycache__" \
  -o -path "*/.coverage_report" \
  -o -path "*/.coverage" \
  -o -path "*/.cspellcache" \
  -o -path "*/.eslintcache" \
  -o -path "*/.git" \
  -o -path "*/.pytest_cache" \
  -o -path "*/.ruff_cache" \
  -o -path "*/.rumdl_cache" \
  -o -path "*/.venv" \
  -o -path "*/.vite" \
  -o -path "*/coverage" \
  -o -path "*/dist" \
  -o -path "*/node_modules" \
  \) -prune -o \
  -type f \
  ! -name ".DS_Store" \
  ! -name "*.pyc" \
  ! -name "pnpm-lock.yaml" \
  ! -name "uv.lock" \
  ! -size +1M \
  -print >$ZIPLIST
# max 1MB

# zip -9 -X -@ "$OUT" <$ZIPLIST
tar -cf - -T $ZIPLIST | xz -6 >"$OUT"

echo "Created: $(pwd)/$OUT"

# TODO: add encryption via age
# mv "$OUT" "$HOME/Library/Mobile Documents/com~apple~CloudDocs/Sicher/T-MB-2/"
# mv "$OUT" /tmp
