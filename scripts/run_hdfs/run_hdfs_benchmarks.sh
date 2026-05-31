#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_ROOT"
source scripts/env/project_env.sh
export HADOOP_CONF_DIR="$PROJECT_ROOT/hadoop/conf"

JDBC_URL="jdbc:hive2://localhost:10000/default"
RESULTS_PATH="results/benchmarks_hdfs/hdfs_benchmark_results.csv"
HDFS_STARTED_BY_THIS_SCRIPT=0
HIVE_STARTED_BY_THIS_SCRIPT=0

cleanup() {
    if [ "$HIVE_STARTED_BY_THIS_SCRIPT" -eq 1 ]; then
        bash scripts/hive/stop_hiveserver2_local.sh
    fi
    if [ "$HDFS_STARTED_BY_THIS_SCRIPT" -eq 1 ]; then
        bash scripts/hdfs/stop_hdfs_local.sh
    fi
}
trap cleanup EXIT

mkdir -p results/benchmarks_hdfs
echo "technology,analysis,dataset_label,input_path,output_path,elapsed_seconds,status" > "$RESULTS_PATH"

if ! hdfs dfs -ls / >/dev/null 2>&1; then
    bash scripts/hdfs/start_hdfs_local.sh
    HDFS_STARTED_BY_THIS_SCRIPT=1
fi
if ! beeline -u "$JDBC_URL" -e "SELECT 1;" >/dev/null 2>&1; then
    bash scripts/hive/start_hiveserver2_local.sh
    HIVE_STARTED_BY_THIS_SCRIPT=1
fi

run_job() {
    local technology="$1"
    local analysis="$2"
    local dataset_label="$3"
    local runner="$4"
    local input_path="hdfs://localhost:9000/flight-delay-project/input/${dataset_label}/flights.csv"
    local output_path="hdfs://localhost:9000/flight-delay-project/output/${technology}/${analysis}_${dataset_label}"
    local start_time end_time elapsed status

    start_time="$(date +%s.%N)"
    if bash "$runner" "$dataset_label"; then
        status="success"
    else
        status="failed"
    fi
    end_time="$(date +%s.%N)"
    elapsed="$(awk -v start="$start_time" -v end="$end_time" 'BEGIN { printf "%.4f", end - start }')"
    echo "$technology,$analysis,$dataset_label,$input_path,$output_path,$elapsed,$status" >> "$RESULTS_PATH"
}

for dataset_label in 100k 500k 1m 3m 7m 10m 14m; do
    run_job spark_sql analysis_1 "$dataset_label" scripts/run_hdfs/run_spark_sql_analysis_1_hdfs.sh
    run_job spark_sql analysis_2 "$dataset_label" scripts/run_hdfs/run_spark_sql_analysis_2_hdfs.sh
    run_job spark_core analysis_1 "$dataset_label" scripts/run_hdfs/run_spark_core_analysis_1_hdfs.sh
    run_job spark_core analysis_2 "$dataset_label" scripts/run_hdfs/run_spark_core_analysis_2_hdfs.sh
    run_job hive analysis_1 "$dataset_label" scripts/run_hdfs/run_hive_analysis_1_hdfs.sh
    run_job hive analysis_2 "$dataset_label" scripts/run_hdfs/run_hive_analysis_2_hdfs.sh
done

echo "HDFS benchmark results: $RESULTS_PATH"
