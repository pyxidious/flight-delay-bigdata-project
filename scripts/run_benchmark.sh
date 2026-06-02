#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

source scripts/env/project_env.sh
source .venv/bin/activate

export HADOOP_CONF_DIR="$PROJECT_ROOT/hadoop/conf"
export HIVE_CONF_DIR="$PROJECT_ROOT/hive/conf"
export MPLCONFIGDIR="${MPLCONFIGDIR:-/tmp/flight-delay-matplotlib}"
export SPARK_DRIVER_MEMORY="${SPARK_DRIVER_MEMORY:-5g}"
export SPARK_SQL_SHUFFLE_PARTITIONS="${SPARK_SQL_SHUFFLE_PARTITIONS:-64}"

mkdir -p "$MPLCONFIGDIR"

python scripts/benchmark/run_benchmark.py "$@"
