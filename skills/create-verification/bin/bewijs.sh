#!/bin/bash
# bewijs.sh — draait één check en schrijft het bewijs in exact het formaat dat de
# Test-kolom van VERIFICATION.html herkent. Gebruik dit in plaats van zelf een
# bewijsformaat verzinnen: het formaatcontract (fingerprint, letterlijk commando,
# letterlijke output, "exit code: N", "resultaat: PASS/FAIL") staat hier op één
# plek, zodat een typfout ("exitcode:") niet stilletjes alles als "handmatig"
# laat renderen.
#
#   bewijs.sh <ID> [--append] [--verwacht-rood] -- <commando...>
#
#   <ID>             criterium-id (A.1); schrijft evidence/<ID>.txt
#   --append         voeg toe aan bestaand bewijs (bv. een mutatierun erbij)
#   --verwacht-rood  deze run MOET falen (mutatie/tegenproef): PASS bij exit != 0
#
# Draai vanuit de repo-root van het project (git nodig voor de fingerprint).
set -u -o pipefail

ID="${1:?gebruik: bewijs.sh <ID> [--append] [--verwacht-rood] -- <commando...>}"; shift
APPEND=0; ROOD=0
while [ $# -gt 0 ] && [ "$1" != "--" ]; do
  case "$1" in
    --append) APPEND=1 ;;
    --verwacht-rood) ROOD=1 ;;
    *) echo "onbekende optie: $1" >&2; exit 64 ;;
  esac; shift
done
[ "${1:-}" = "--" ] && shift
[ $# -gt 0 ] || { echo "geen commando meegegeven na --" >&2; exit 64; }

mkdir -p evidence
OUT="evidence/$ID.txt"
[ "$APPEND" -eq 1 ] || : > "$OUT"

{
  echo "== fingerprint: $(hostname) | $(uname -s) $(sw_vers -productVersion 2>/dev/null || uname -r) | user=$(whoami) | $(date '+%Y-%m-%d %H:%M:%S %Z') | commit=$(git rev-parse --short HEAD 2>/dev/null || echo geen-git) | tree=$(git status --porcelain -uno 2>/dev/null | wc -l | tr -d ' ') dirty files =="
  [ "$ROOD" -eq 1 ] && echo "== tegenproef: deze run moet ROOD zijn (verwacht exit != 0) =="
  printf '$'; printf ' %q' "$@"; echo
  "$@" 2>&1
  rc=$?
  echo "exit code: $rc"
  if [ "$ROOD" -eq 1 ]; then
    [ "$rc" -ne 0 ] && echo "resultaat: PASS" || echo "resultaat: FAIL"
  else
    [ "$rc" -eq 0 ] && echo "resultaat: PASS" || echo "resultaat: FAIL"
  fi
} >> "$OUT"

tail -2 "$OUT" | sed "s|^|$ID: |"
