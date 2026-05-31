#!/usr/bin/env bash

set -euo pipefail

INPUT_FILE="${1:-data/samples/flights_100k.csv}"
OUTPUT_DIR="${2:-results/output/hive/analysis_2}"
PREVIEW_PATH="${3:-results/tables/hive_analysis_2_preview.csv}"

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

cd "$PROJECT_ROOT"

source scripts/env/project_env.sh

export HIVE_CONF_DIR="$PROJECT_ROOT/hive/conf"

export HADOOP_HEAPSIZE=2048
export HADOOP_CLIENT_OPTS="-Xmx2048m ${HADOOP_CLIENT_OPTS:-}"
export HIVE_OPTS="-Xmx2048m ${HIVE_OPTS:-}"

INPUT_DIR="$PROJECT_ROOT/results/tmp/hive_input/analysis_2_input"

mkdir -p "$INPUT_DIR"
mkdir -p "$(dirname "$PREVIEW_PATH")"

rm -rf "$INPUT_DIR"
mkdir -p "$INPUT_DIR"

cp "$INPUT_FILE" "$INPUT_DIR/flights.csv"

rm -rf "$OUTPUT_DIR"

echo "Running Hive Analysis 2"
echo "Input file:  $INPUT_FILE"
echo "Hive input:  $INPUT_DIR"
echo "Output:      $OUTPUT_DIR"
echo "Preview:     $PREVIEW_PATH"
echo

beeline \
  -u "jdbc:hive2://localhost:10000/default" \
  --hiveconf input_dir="file://$INPUT_DIR" \
  --hiveconf output_dir="file://$PROJECT_ROOT/$OUTPUT_DIR" \
  -f hive/analysis_2_airport_month_delay_report.sql

echo
echo "Output files:"
find "$OUTPUT_DIR" -type f

echo
echo "Saving preview to $PREVIEW_PATH"
{
  echo "origin,month,dep_delay_band,flight_count,avg_dep_delay,avg_arr_delay,top_3_causes"
  head -n 10 "$OUTPUT_DIR"/*
} > "$PREVIEW_PATH"

echo
echo "Preview:"
cat "$PREVIEW_PATH"
