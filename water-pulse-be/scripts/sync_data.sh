#!/usr/bin/env bash
# Copy the latest data package from the pipeline repo: scripts/sync_data.sh /path/to/skyradar-nisar
set -euo pipefail
SRC="${1:?path to skyradar-nisar}/data/web"
DST="$(cd "$(dirname "$0")/.." && pwd)/data"
[ -f "$SRC/manifest.json" ] || { echo "no manifest.json in $SRC" >&2; exit 1; }
rm -rf "$DST.tmp" && cp -r "$SRC" "$DST.tmp" && rm -rf "$DST" && mv "$DST.tmp" "$DST"
echo "synced $(ls "$DST/water" | wc -l) frames into $DST"
