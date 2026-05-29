#!/usr/bin/env bash

set -euo pipefail

DATASET_LABEL="${1:-100k}"
INPUT_FILE="${2:-data/samples/flights_100k.csv}"

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$PROJECT_ROOT"

source scripts/project_env.sh

echo "========================================"
echo "Running all analyses"
echo "Dataset label: $DATASET_LABEL"
echo "Input file:    $INPUT_FILE"
echo "========================================"
echo

if [ ! -f "$INPUT_FILE" ]; then
    echo "ERROR: input file not found: $INPUT_FILE"
    exit 1
fi

echo "[1/6] Spark SQL Analysis 1"
bash scripts/run_spark_sql_analysis_1.sh \
  "$INPUT_FILE" \
  "results/output/spark_sql/analysis_1_${DATASET_LABEL}" \
  "results/tables/spark_sql_analysis_1_${DATASET_LABEL}_preview.csv"

echo
echo "[2/6] Spark SQL Analysis 2"
bash scripts/run_spark_sql_analysis_2.sh \
  "$INPUT_FILE" \
  "results/output/spark_sql/analysis_2_${DATASET_LABEL}" \
  "results/tables/spark_sql_analysis_2_${DATASET_LABEL}_preview.csv"

echo
echo "[3/6] Spark Core Analysis 1"
bash scripts/run_spark_core_analysis_1.sh \
  "$INPUT_FILE" \
  "results/output/spark_core/analysis_1_${DATASET_LABEL}" \
  "results/tables/spark_core_analysis_1_${DATASET_LABEL}_preview.csv"

echo
echo "[4/6] Spark Core Analysis 2"
bash scripts/run_spark_core_analysis_2.sh \
  "$INPUT_FILE" \
  "results/output/spark_core/analysis_2_${DATASET_LABEL}" \
  "results/tables/spark_core_analysis_2_${DATASET_LABEL}_preview.csv"

echo
echo "[5/6] Hive Analysis 1"
bash scripts/run_hive_analysis_1.sh \
  "$INPUT_FILE" \
  "results/output/hive/analysis_1_${DATASET_LABEL}" \
  "results/tables/hive_analysis_1_${DATASET_LABEL}_preview.csv"

echo
echo "[6/6] Hive Analysis 2"
bash scripts/run_hive_analysis_2.sh \
  "$INPUT_FILE" \
  "results/output/hive/analysis_2_${DATASET_LABEL}" \
  "results/tables/hive_analysis_2_${DATASET_LABEL}_preview.csv"

echo
echo "========================================"
echo "All analyses completed for $DATASET_LABEL"
echo "========================================"
