#!/usr/bin/env bash

set -euo pipefail

DATASET_LABEL="${1:-100k}"
INPUT_PATH="${2:-hdfs://localhost:9000/flight-delay-project/input/${DATASET_LABEL}/flights.csv}"
OUTPUT_DIR="${3:-hdfs://localhost:9000/flight-delay-project/output/spark_core/analysis_2_${DATASET_LABEL}}"
PREVIEW_PATH="${4:-results/tables_hdfs/spark_core_analysis_2_${DATASET_LABEL}_preview.csv}"

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_ROOT"
source scripts/env/project_env.sh
export HADOOP_CONF_DIR="$PROJECT_ROOT/hadoop/conf"

mkdir -p "$(dirname "$PREVIEW_PATH")"
hdfs dfs -rm -r -f "$OUTPUT_DIR" >/dev/null 2>&1 || true
spark-submit --master local[*] spark_core/analysis_2_airport_month_delay_report.py \
  --input "$INPUT_PATH" --output "$OUTPUT_DIR"

hdfs dfs -ls "$OUTPUT_DIR"
TMP_PREVIEW_SOURCE="$(mktemp)"
trap 'rm -f "$TMP_PREVIEW_SOURCE"' EXIT
hdfs dfs -cat "$OUTPUT_DIR"/part-* > "$TMP_PREVIEW_SOURCE"
head -n 11 "$TMP_PREVIEW_SOURCE" > "$PREVIEW_PATH"
rm -f "$TMP_PREVIEW_SOURCE"
trap - EXIT
cat "$PREVIEW_PATH"
