#!/usr/bin/env bash

set -euo pipefail

INPUT_PATH="${1:-data/samples/flights_100k.csv}"
OUTPUT_PATH="${2:-results/output/spark_sql/analysis_2}"
PREVIEW_PATH="${3:-results/tables/spark_sql_analysis_2_preview.csv}"

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$PROJECT_ROOT"

source scripts/project_env.sh

mkdir -p "$(dirname "$PREVIEW_PATH")"

echo "Running Spark SQL Analysis 2"
echo "Input:   $INPUT_PATH"
echo "Output:  $OUTPUT_PATH"
echo "Preview: $PREVIEW_PATH"
echo

rm -rf "$OUTPUT_PATH"

spark-submit spark_sql/analysis_2_airport_month_delay_report.py \
  --input "$INPUT_PATH" \
  --output "$OUTPUT_PATH"

echo
echo "Output files:"
find "$OUTPUT_PATH" -type f

echo
echo "Saving preview to $PREVIEW_PATH"
head -n 11 "$OUTPUT_PATH"/part-*.csv > "$PREVIEW_PATH"

echo
echo "Preview:"
cat "$PREVIEW_PATH"
