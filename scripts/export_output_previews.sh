#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

RUNS_CSV="results/benchmark/benchmark_runs.csv"
OUTPUT_DIR="results/previews"
DATASETS=(100k 500k 1m 3m 7m 10m 14m)
ANALYSES=(analysis_1 analysis_2 analysis_3)
TECHNOLOGIES=(hive spark_core spark_sql)
RUN_INDEX=1
DRY_RUN=false
OVERWRITE=false

usage() {
  cat <<'EOF'
Usage: bash scripts/export_output_previews.sh [options]

Options:
  --runs-csv PATH          Run-level benchmark CSV (default: results/benchmark/benchmark_runs.csv)
  --output-dir DIR         Local preview output directory (default: results/previews)
  --datasets VALUES...     Dataset labels (default: 100k 500k 1m 3m 7m 10m 14m)
  --analyses VALUES...     Analyses (default: analysis_1 analysis_2 analysis_3)
  --technologies VALUES... Technologies (default: hive spark_core spark_sql)
  --run-index N            Repeated run index to export (default: 1)
  --dry-run                Print planned reads/writes without reading HDFS or writing files
  --overwrite              Regenerate existing preview files
  -h, --help               Show this help
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --runs-csv)
      RUNS_CSV="${2:-}"
      shift 2
      ;;
    --output-dir)
      OUTPUT_DIR="${2:-}"
      shift 2
      ;;
    --datasets)
      shift
      DATASETS=()
      while [[ $# -gt 0 && "$1" != --* ]]; do
        DATASETS+=("$1")
        shift
      done
      ;;
    --analyses)
      shift
      ANALYSES=()
      while [[ $# -gt 0 && "$1" != --* ]]; do
        ANALYSES+=("$1")
        shift
      done
      ;;
    --technologies)
      shift
      TECHNOLOGIES=()
      while [[ $# -gt 0 && "$1" != --* ]]; do
        TECHNOLOGIES+=("$1")
        shift
      done
      ;;
    --run-index)
      RUN_INDEX="${2:-}"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --overwrite)
      OVERWRITE=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "[WARN] unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ ${#DATASETS[@]} -eq 0 || ${#ANALYSES[@]} -eq 0 || ${#TECHNOLOGIES[@]} -eq 0 ]]; then
  echo "[WARN] datasets, analyses and technologies must not be empty" >&2
  exit 2
fi

if ! [[ "$RUN_INDEX" =~ ^[0-9]+$ ]] || [[ "$RUN_INDEX" -lt 1 ]]; then
  echo "[WARN] --run-index must be a positive integer: $RUN_INDEX" >&2
  exit 2
fi

declare -A OUTPUT_PATHS=()

if [[ ! -f "$RUNS_CSV" ]]; then
  echo "[WARN] runs CSV not found: $RUNS_CSV"
  exit 0
fi

RUNS_TSV="$(mktemp)"
trap 'rm -f "$RUNS_TSV" "${MD_TMP:-}" "${PREVIEW_TMP:-}" "${HDFS_ERR:-}"' EXIT

if ! python3 - "$RUNS_CSV" "$RUN_INDEX" > "$RUNS_TSV" <<'PY'
import csv
import sys

runs_csv = sys.argv[1]
run_index = sys.argv[2]
required = {"technology", "analysis", "dataset_label", "run_index", "status", "output_path"}
seen = set()

with open(runs_csv, newline="", encoding="utf-8") as handle:
    reader = csv.DictReader(handle)
    missing = required.difference(reader.fieldnames or [])
    if missing:
        print(f"missing required CSV columns: {', '.join(sorted(missing))}", file=sys.stderr)
        sys.exit(1)
    for row in reader:
        if row.get("status") != "success":
            continue
        if str(row.get("run_index", "")).strip() != run_index:
            continue
        key = (
            row.get("technology", "").strip(),
            row.get("analysis", "").strip(),
            row.get("dataset_label", "").strip(),
        )
        if key in seen:
            continue
        seen.add(key)
        print("\t".join([key[0], key[1], key[2], row.get("output_path", "").strip()]))
PY
then
  echo "[WARN] unable to read runs CSV: $RUNS_CSV"
  exit 0
fi

while IFS=$'\t' read -r technology analysis dataset output_path; do
  [[ -n "${technology:-}" ]] || continue
  OUTPUT_PATHS["$technology|$analysis|$dataset"]="$output_path"
done < "$RUNS_TSV"

md_append() {
  if [[ "$DRY_RUN" == false ]]; then
    printf '%s\n' "$*" >> "$MD_TMP"
  fi
}

md_append_file_block() {
  local file=$1
  if [[ "$DRY_RUN" == false ]]; then
    printf '```text\n' >> "$MD_TMP"
    if [[ -s "$file" ]]; then
      sed 's/\r$//' "$file" >> "$MD_TMP"
    else
      printf '[WARN] preview vuota\n' >> "$MD_TMP"
    fi
    printf '\n```\n\n' >> "$MD_TMP"
  fi
}

md_append_warning() {
  local message=$1
  if [[ "$DRY_RUN" == false ]]; then
    printf '```text\n[WARN] %s\n```\n\n' "$message" >> "$MD_TMP"
  fi
}

if [[ "$DRY_RUN" == false ]]; then
  mkdir -p "$OUTPUT_DIR"
  MD_TMP="$(mktemp)"
  {
    printf '# Preview delle prime 10 righe degli output\n\n'
    printf 'Le preview riportano le prime 10 righe fisiche lette dagli output distribuiti HDFS. Poiché non viene applicato un ordinamento globale finale, l'\''ordine delle righe può variare tra ambiente locale e cluster o tra esecuzioni diverse. La semantica e lo schema dell'\''output restano invariati.\n\n'
    printf 'Nota: se gli output cluster non sono disponibili perché HDFS EMR è temporaneo, queste preview devono essere estratte dagli output locali disponibili.\n\n'
  } > "$MD_TMP"
fi

if [[ "$DRY_RUN" == false ]] && ! command -v hdfs >/dev/null 2>&1; then
  echo "[WARN] hdfs command not found"
fi

for dataset in "${DATASETS[@]}"; do
  md_append "## $dataset"
  md_append ""
  for analysis in "${ANALYSES[@]}"; do
    md_append "### $analysis"
    md_append ""
    for technology in "${TECHNOLOGIES[@]}"; do
      key="$technology|$analysis|$dataset"
      preview_file="$OUTPUT_DIR/$dataset/$analysis/${technology}_first10.csv"
      output_path="${OUTPUT_PATHS[$key]:-}"
      md_append "#### $technology"
      md_append ""

      if [[ -z "$output_path" ]]; then
        echo "[WARN] $dataset $analysis $technology combination not found in $RUNS_CSV"
        md_append_warning "$dataset $analysis $technology combination not found in $RUNS_CSV"
        continue
      fi

      if [[ "$DRY_RUN" == true ]]; then
        echo "[DRY] $dataset $analysis $technology read $output_path/part-* -> $preview_file"
        continue
      fi

      mkdir -p "$(dirname "$preview_file")"

      if [[ -f "$preview_file" && "$OVERWRITE" == false ]]; then
        echo "[SKIP] $dataset $analysis $technology -> $preview_file"
        md_append_file_block "$preview_file"
        continue
      fi

      if ! command -v hdfs >/dev/null 2>&1; then
        echo "[WARN] $dataset $analysis $technology hdfs command not found"
        md_append_warning "$dataset $analysis $technology hdfs command not found"
        continue
      fi

      if ! hdfs dfs -test -e "$output_path" >/dev/null 2>&1; then
        echo "[WARN] $dataset $analysis $technology output not found: $output_path"
        md_append_warning "$dataset $analysis $technology output not found: $output_path"
        continue
      fi

      PREVIEW_TMP="$(mktemp)"
      HDFS_ERR="$(mktemp)"
      set +e
      hdfs dfs -cat "${output_path%/}/part-*" 2>"$HDFS_ERR" | head -n 10 > "$PREVIEW_TMP"
      cat_status=${PIPESTATUS[0]}
      head_status=${PIPESTATUS[1]}
      set -e

      if [[ "$cat_status" -ne 0 && "$cat_status" -ne 141 ]] || [[ "$head_status" -ne 0 ]]; then
        detail="$(tr '\n' ' ' < "$HDFS_ERR" | sed 's/[[:space:]][[:space:]]*/ /g' | cut -c 1-240)"
        echo "[WARN] $dataset $analysis $technology output not readable: ${output_path%/}/part-*"
        md_append_warning "$dataset $analysis $technology output not readable: ${output_path%/}/part-* ${detail}"
        rm -f "$PREVIEW_TMP" "$HDFS_ERR"
        PREVIEW_TMP=""
        HDFS_ERR=""
        continue
      fi

      mv "$PREVIEW_TMP" "$preview_file"
      rm -f "$HDFS_ERR"
      PREVIEW_TMP=""
      HDFS_ERR=""

      echo "[OK] $dataset $analysis $technology -> $preview_file"
      md_append_file_block "$preview_file"
    done
  done
done

if [[ "$DRY_RUN" == false ]]; then
  mv "$MD_TMP" "$OUTPUT_DIR/output_previews.md"
  MD_TMP=""
  echo "[OK] markdown -> $OUTPUT_DIR/output_previews.md"
fi
