#!/usr/bin/env bash

set -euo pipefail

DATASET_LABEL="${1:-100k}"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_ROOT"
source scripts/env/project_env.sh
export HADOOP_CONF_DIR="$PROJECT_ROOT/hadoop/conf"

JDBC_URL="jdbc:hive2://localhost:10000/default"
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

if ! hdfs dfs -ls / >/dev/null 2>&1; then
    bash scripts/hdfs/start_hdfs_local.sh
    HDFS_STARTED_BY_THIS_SCRIPT=1
fi

if ! beeline -u "$JDBC_URL" -e "SELECT 1;" >/dev/null 2>&1; then
    bash scripts/hive/start_hiveserver2_local.sh
    HIVE_STARTED_BY_THIS_SCRIPT=1
fi

echo "Running all HDFS analyses for dataset $DATASET_LABEL"
bash scripts/run_hdfs/run_spark_sql_analysis_1_hdfs.sh "$DATASET_LABEL"
bash scripts/run_hdfs/run_spark_sql_analysis_2_hdfs.sh "$DATASET_LABEL"
bash scripts/run_hdfs/run_spark_core_analysis_1_hdfs.sh "$DATASET_LABEL"
bash scripts/run_hdfs/run_spark_core_analysis_2_hdfs.sh "$DATASET_LABEL"
bash scripts/run_hdfs/run_hive_analysis_1_hdfs.sh "$DATASET_LABEL"
bash scripts/run_hdfs/run_hive_analysis_2_hdfs.sh "$DATASET_LABEL"
