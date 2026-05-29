#!/usr/bin/env bash

set -euo pipefail

INPUT_FILE="${1:-data/samples/flights_100k.csv}"
OUTPUT_DIR="${2:-results/output/hive/analysis_1}"
PREVIEW_PATH="${3:-results/tables/hive_analysis_1_preview.csv}"

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

cd "$PROJECT_ROOT"

source scripts/env/project_env.sh

export HIVE_CONF_DIR="$PROJECT_ROOT/hive/conf"

INPUT_DIR="$PROJECT_ROOT/results/tmp/hive_input/analysis_1_input"

mkdir -p "$INPUT_DIR"
mkdir -p "$(dirname "$PREVIEW_PATH")"

rm -rf "$INPUT_DIR"
mkdir -p "$INPUT_DIR"

cp "$INPUT_FILE" "$INPUT_DIR/flights.csv"

rm -rf "$OUTPUT_DIR"

echo "Running Hive Analysis 1"
echo "Input file:  $INPUT_FILE"
echo "Hive input:  $INPUT_DIR"
echo "Output:      $OUTPUT_DIR"
echo "Preview:     $PREVIEW_PATH"
echo

beeline \
  -u "jdbc:hive2://localhost:10000/default" \
  --hiveconf input_dir="file://$INPUT_DIR" \
  --hiveconf output_dir="file://$PROJECT_ROOT/$OUTPUT_DIR" \
  -f hive/analysis_1_airline_stats.sql

echo
echo "Output files:"
find "$OUTPUT_DIR" -type f

echo
echo "Saving preview to $PREVIEW_PATH"
{
  echo "airline,origin,total_flights,min_arr_delay,max_arr_delay,avg_arr_delay,cancelled_flights,cancellation_rate,active_months"
  head -n 10 "$OUTPUT_DIR"/*
} > "$PREVIEW_PATH"

echo
echo "Preview:"
cat "$PREVIEW_PATH"
