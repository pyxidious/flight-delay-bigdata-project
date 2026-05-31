#!/usr/bin/env bash

set -euo pipefail

DATASET_LABEL="${1:-100k}"
INPUT_DIR="${2:-hdfs://localhost:9000/flight-delay-project/input/${DATASET_LABEL}}"
OUTPUT_DIR="${3:-hdfs://localhost:9000/flight-delay-project/output/hive/analysis_1_${DATASET_LABEL}}"
PREVIEW_PATH="${4:-results/tables_hdfs/hive_analysis_1_${DATASET_LABEL}_preview.csv}"

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_ROOT"
source scripts/env/project_env.sh
export HADOOP_CONF_DIR="$PROJECT_ROOT/hadoop/conf"
export HIVE_CONF_DIR="$PROJECT_ROOT/hive/conf"
export HADOOP_HEAPSIZE=6144
export HADOOP_CLIENT_OPTS="-Xmx6144m ${HADOOP_CLIENT_OPTS:-}"

mkdir -p "$(dirname "$PREVIEW_PATH")"
hdfs dfs -rm -r -f "$OUTPUT_DIR" >/dev/null 2>&1 || true

beeline -u "jdbc:hive2://localhost:10000/default" \
  --hiveconf input_dir="$INPUT_DIR" \
  --hiveconf output_dir="$OUTPUT_DIR" \
  -f hive/analysis_1_airline_stats.sql

hdfs dfs -ls "$OUTPUT_DIR"
TMP_PREVIEW_SOURCE="$(mktemp)"
trap 'rm -f "$TMP_PREVIEW_SOURCE"' EXIT
hdfs dfs -cat "$OUTPUT_DIR"/* > "$TMP_PREVIEW_SOURCE"
{
  echo "airline,origin,total_flights,min_arr_delay,max_arr_delay,avg_arr_delay,cancelled_flights,cancellation_rate,active_months"
  head -n 10 "$TMP_PREVIEW_SOURCE"
} > "$PREVIEW_PATH"
rm -f "$TMP_PREVIEW_SOURCE"
trap - EXIT
cat "$PREVIEW_PATH"
