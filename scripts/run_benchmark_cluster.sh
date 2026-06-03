#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# EMR already provides Hadoop, Hive and Spark configuration. Do not require
# the local virtualenv or local hadoop/conf and hive/conf used by the laptop run.
export MPLCONFIGDIR="${MPLCONFIGDIR:-/tmp/flight-delay-matplotlib}"
export SPARK_DRIVER_MEMORY="${SPARK_DRIVER_MEMORY:-5g}"
export SPARK_SQL_SHUFFLE_PARTITIONS="${SPARK_SQL_SHUFFLE_PARTITIONS:-64}"
export CLUSTER_HDFS_OUTPUT_BASE="${CLUSTER_HDFS_OUTPUT_BASE:-/flight-delay/results/output_benchmark_cluster}"
export CLUSTER_HDFS_INPUT_BASE="${CLUSTER_HDFS_INPUT_BASE:-/flight-delay-project/input}"
export HIVE_CLIENT="${HIVE_CLIENT:-beeline}"

mkdir -p "$MPLCONFIGDIR"

python3 scripts/benchmark/run_benchmark_cluster.py "$@"
