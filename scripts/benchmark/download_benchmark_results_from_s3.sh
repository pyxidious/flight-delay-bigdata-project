#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  cat >&2 <<USAGE
Uso:
  $0 s3://bucket/prefix /cartella/locale [campaign_tag]

Se campaign_tag non è indicato, lo script sceglie l'ultima cartella trovata sotto il prefisso S3.
Lo script attende automaticamente la presenza di benchmark_results.tar.gz e poi sincronizza i file sul PC.
USAGE
  exit 2
fi

S3_PREFIX="${1%/}"
LOCAL_DIR="$2"
CAMPAIGN_TAG="${3:-}"
POLL_SECONDS="${POLL_SECONDS:-30}"
MAX_ATTEMPTS="${MAX_ATTEMPTS:-480}"

if [[ -z "$CAMPAIGN_TAG" ]]; then
  CAMPAIGN_TAG="$(aws s3 ls "$S3_PREFIX/" | awk '/PRE/ {gsub("/", "", $2); print $2}' | sort | tail -n 1)"
fi

if [[ -z "$CAMPAIGN_TAG" ]]; then
  echo "Nessuna campagna trovata in $S3_PREFIX" >&2
  exit 1
fi

REMOTE="$S3_PREFIX/$CAMPAIGN_TAG"
DEST="$LOCAL_DIR/$CAMPAIGN_TAG"
mkdir -p "$DEST"

echo "Campagna: $CAMPAIGN_TAG"
echo "S3:       $REMOTE"
echo "Locale:   $DEST"

for attempt in $(seq 1 "$MAX_ATTEMPTS"); do
  if aws s3 ls "$REMOTE/benchmark_results.tar.gz" >/dev/null 2>&1; then
    break
  fi
  echo "[$attempt/$MAX_ATTEMPTS] benchmark_results.tar.gz non ancora disponibile; riprovo tra ${POLL_SECONDS}s..."
  sleep "$POLL_SECONDS"
  if [[ "$attempt" == "$MAX_ATTEMPTS" ]]; then
    echo "Timeout: archivio risultati non trovato in $REMOTE" >&2
    exit 1
  fi
done

aws s3 sync "$REMOTE/files" "$DEST/files"
aws s3 cp "$REMOTE/benchmark_results.tar.gz" "$DEST/benchmark_results.tar.gz"

echo "Download completato in $DEST"
