#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

cd "$PROJECT_ROOT"

source scripts/env/project_env.sh

BENCHMARK_OUTPUT="results/benchmarks/benchmark_results.csv"

mkdir -p results/benchmarks

echo "technology,analysis,dataset_label,input_file,elapsed_seconds" > "$BENCHMARK_OUTPUT"

run_and_measure() {
    local technology="$1"
    local analysis="$2"
    local dataset_label="$3"
    local input_file="$4"
    local command="$5"

    echo
    echo "========================================"
    echo "Benchmark"
    echo "Technology: $technology"
    echo "Analysis:   $analysis"
    echo "Dataset:    $dataset_label"
    echo "Input:      $input_file"
    echo "========================================"

    local start_time
    local end_time
    local elapsed

    start_time="$(date +%s.%N)"

    eval "$command"

    end_time="$(date +%s.%N)"

    elapsed="$(python - <<PY
start_time = float("$start_time")
end_time = float("$end_time")
print(round(end_time - start_time, 4))
PY
)"

    echo "$technology,$analysis,$dataset_label,$input_file,$elapsed" >> "$BENCHMARK_OUTPUT"
    echo "Elapsed seconds: $elapsed"
}

run_dataset_benchmarks() {
    local dataset_label="$1"
    local input_file="$2"

    if [ ! -f "$input_file" ]; then
        echo "ERROR: input file not found: $input_file"
        exit 1
    fi

    run_and_measure \
        "spark_sql" \
        "analysis_1" \
        "$dataset_label" \
        "$input_file" \
        "bash scripts/run/run_spark_sql_analysis_1.sh '$input_file' 'results/output/spark_sql/analysis_1_${dataset_label}' 'results/tables/spark_sql_analysis_1_${dataset_label}_preview.csv'"

    run_and_measure \
        "spark_sql" \
        "analysis_2" \
        "$dataset_label" \
        "$input_file" \
        "bash scripts/run/run_spark_sql_analysis_2.sh '$input_file' 'results/output/spark_sql/analysis_2_${dataset_label}' 'results/tables/spark_sql_analysis_2_${dataset_label}_preview.csv'"

    run_and_measure \
        "spark_core" \
        "analysis_1" \
        "$dataset_label" \
        "$input_file" \
        "bash scripts/run/run_spark_core_analysis_1.sh '$input_file' 'results/output/spark_core/analysis_1_${dataset_label}' 'results/tables/spark_core_analysis_1_${dataset_label}_preview.csv'"

    run_and_measure \
        "spark_core" \
        "analysis_2" \
        "$dataset_label" \
        "$input_file" \
        "bash scripts/run/run_spark_core_analysis_2.sh '$input_file' 'results/output/spark_core/analysis_2_${dataset_label}' 'results/tables/spark_core_analysis_2_${dataset_label}_preview.csv'"

    run_and_measure \
        "hive" \
        "analysis_1" \
        "$dataset_label" \
        "$input_file" \
        "bash scripts/run/run_hive_analysis_1.sh '$input_file' 'results/output/hive/analysis_1_${dataset_label}' 'results/tables/hive_analysis_1_${dataset_label}_preview.csv'"

    run_and_measure \
        "hive" \
        "analysis_2" \
        "$dataset_label" \
        "$input_file" \
        "bash scripts/run/run_hive_analysis_2.sh '$input_file' 'results/output/hive/analysis_2_${dataset_label}' 'results/tables/hive_analysis_2_${dataset_label}_preview.csv'"
}

JDBC_URL="jdbc:hive2://localhost:10000/default"
HIVE_STARTED_BY_THIS_SCRIPT=0

cleanup() {
    if [ "$HIVE_STARTED_BY_THIS_SCRIPT" -eq 1 ]; then
        echo
        echo "Stopping HiveServer2 started by this script..."
        bash scripts/hive/stop_hiveserver2_local.sh
    fi
}

trap cleanup EXIT

echo "Checking HiveServer2 before running benchmarks..."

if beeline -u "$JDBC_URL" -e "SELECT 1;" >/dev/null 2>&1; then
    echo "HiveServer2 is already running. It will not be stopped by this script."
else
    echo "HiveServer2 is not running. Starting it now..."
    bash scripts/hive/start_hiveserver2_local.sh
    HIVE_STARTED_BY_THIS_SCRIPT=1
fi

run_dataset_benchmarks "100k" "data/samples/flights_100k.csv"
run_dataset_benchmarks "500k" "data/samples/flights_500k.csv"
run_dataset_benchmarks "1m" "data/samples/flights_1m.csv"
run_dataset_benchmarks "3m" "data/samples/flights_3m.csv"
run_dataset_benchmarks "7m" "data/samples/flights_7m.csv"
run_dataset_benchmarks "10m" "data/samples/flights_10m.csv"
run_dataset_benchmarks "14m" "data/samples/flights_14m.csv"

echo
echo "Benchmark completed."
echo "Results saved to: $BENCHMARK_OUTPUT"
cat "$BENCHMARK_OUTPUT"
