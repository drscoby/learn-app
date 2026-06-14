#!/usr/bin/env bash
# sync_content.sh — regenerate content.json from the academic sets and push it
# to the GitHub Pages repo, so the iPhone app updates OTA.
#
# One-time edit: set REPO to your local clone of the Pages repo.
# Then run manually, or let the scheduled task run it.

set -euo pipefail

SECOND_BRAIN="${SECOND_BRAIN:-$HOME/Documents/Claude/Projects/Second Brain}"
REPO="${REPO:-$HOME/learn-app}"          # <-- your local clone of the Pages repo
GEN="$(dirname "$0")/generate_content.py"

echo "Generating content.json from: $SECOND_BRAIN"
python3 "$GEN" "$SECOND_BRAIN" "$REPO"

cd "$REPO"
if [[ -n "$(git status --porcelain content.json)" ]]; then
  git add content.json
  git commit -m "content update $(date '+%Y-%m-%d %H:%M')"
  git push
  echo "Pushed updated content.json — the app will pick it up OTA."
else
  echo "No content change — nothing to push."
fi
